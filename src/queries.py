from datetime import datetime, timedelta, timezone
from math import radians

from bson import ObjectId


QUERY_REGISTRY = [
    {
        "id": "stations_by_genre",
        "title": "Stations par genre et pays",
        "description": "Trouver les stations qui correspondent a un genre musical et, optionnellement, a un pays.",
        "params": [{"name": "genre", "type": "text", "default": "jazz"}, {"name": "country", "type": "text", "default": ""}],
    },
    {
        "id": "top_stations",
        "title": "Stations les plus ecoutees",
        "description": "Classer les stations par minutes d'ecoute sur une periode recente.",
        "params": [{"name": "days", "type": "number", "default": "14"}, {"name": "limit", "type": "number", "default": "5"}],
    },
    {
        "id": "liked_tracks_by_genre",
        "title": "Titres les plus aimes par genre",
        "description": "Identifier les titres qui generent le plus de likes dans un genre.",
        "params": [{"name": "genre", "type": "text", "default": "lofi"}, {"name": "limit", "type": "number", "default": "5"}],
    },
    {
        "id": "personalized_recommendations",
        "title": "Recommandations personnalisees",
        "description": "Recommander des stations et titres selon les preferences et l'historique d'un utilisateur.",
        "params": [{"name": "email", "type": "text", "default": "alice@example.com"}],
    },
    {
        "id": "peak_hours",
        "title": "Heures de pic par station",
        "description": "Mesurer les heures ou une station concentre le plus de duree d'ecoute.",
        "params": [{"name": "station", "type": "text", "default": "Jazz Horizon"}],
    },
    {
        "id": "audience_by_city",
        "title": "Audience par ville",
        "description": "Voir les villes qui apportent le plus d'auditeurs actifs.",
        "params": [{"name": "days", "type": "number", "default": "30"}],
    },
    {
        "id": "user_history",
        "title": "Historique enrichi",
        "description": "Afficher l'historique d'un utilisateur avec les noms de stations et de titres.",
        "params": [{"name": "email", "type": "text", "default": "alice@example.com"}, {"name": "limit", "type": "number", "default": "10"}],
    },
    {
        "id": "playlist_tags",
        "title": "Tendances des playlists",
        "description": "Analyser les tags les plus frequents dans les playlists publiques.",
        "params": [{"name": "limit", "type": "number", "default": "8"}],
    },
    {
        "id": "programs_on_air",
        "title": "Programmes diffuses",
        "description": "Lister les programmes prevus pour un jour et une heure donnes.",
        "params": [{"name": "day", "type": "text", "default": "monday"}, {"name": "time", "type": "text", "default": "08:30"}],
    },
    {
        "id": "nearby_stations",
        "title": "Stations proches",
        "description": "Trouver les stations les plus proches d'une position geographique.",
        "params": [{"name": "lat", "type": "number", "default": "48.8566"}, {"name": "lng", "type": "number", "default": "2.3522"}, {"name": "max_km", "type": "number", "default": "900"}],
    },
    {
        "id": "subscription_segments",
        "title": "Segments d'abonnement",
        "description": "Regrouper les utilisateurs par formule, tranche d'age et genre prefere.",
        "params": [],
    },
    {
        "id": "track_retention",
        "title": "Retention par titre",
        "description": "Comparer la duree ecoutee moyenne a la duree totale des titres.",
        "params": [{"name": "limit", "type": "number", "default": "8"}],
    },
]


def as_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def now_utc():
    return datetime.now(timezone.utc).replace(microsecond=0)


def stations_by_genre(db, genre="jazz", country=""):
    criteria = {"genres": genre.lower()}
    if country:
        criteria["country"] = country
    return list(
        db.stations.find(
            criteria,
            {"name": 1, "country": 1, "city": 1, "genres": 1, "bitrate_kbps": 1, "rating": 1},
        ).sort("rating.average", -1)
    )


def top_stations(db, days="14", limit="5"):
    since = now_utc() - timedelta(days=as_int(days, 14))
    return list(
        db.listening_events.aggregate(
            [
                {"$match": {"started_at": {"$gte": since}}},
                {"$group": {"_id": "$station_id", "total_seconds": {"$sum": "$duration_seconds"}, "sessions": {"$sum": 1}}},
                {"$lookup": {"from": "stations", "localField": "_id", "foreignField": "_id", "as": "station"}},
                {"$unwind": "$station"},
                {
                    "$project": {
                        "_id": 0,
                        "station": "$station.name",
                        "country": "$station.country",
                        "city": "$station.city",
                        "sessions": 1,
                        "total_minutes": {"$divide": ["$total_seconds", 60]},
                    }
                },
                {"$sort": {"total_minutes": -1}},
                {"$limit": as_int(limit, 5)},
            ]
        )
    )


def liked_tracks_by_genre(db, genre="lofi", limit="5"):
    pipeline = [
        {"$match": {"liked": True}},
        {"$lookup": {"from": "tracks", "localField": "track_id", "foreignField": "_id", "as": "track"}},
        {"$unwind": "$track"},
        {"$match": {"track.genre": genre.lower()}},
        {"$group": {"_id": "$track_id", "likes": {"$sum": 1}, "title": {"$first": "$track.title"}, "artist": {"$first": "$track.artist"}, "genre": {"$first": "$track.genre"}}},
        {"$sort": {"likes": -1, "title": 1}},
        {"$limit": as_int(limit, 5)},
        {"$project": {"_id": 0, "title": 1, "artist": 1, "genre": 1, "likes": 1}},
    ]
    return list(db.listening_events.aggregate(pipeline))


def personalized_recommendations(db, email="alice@example.com"):
    user = db.users.find_one({"email": email})
    if not user:
        return {"error": "Utilisateur introuvable"}

    favorite_genres = user.get("preferences", {}).get("favorite_genres", [])
    listened_station_ids = db.listening_events.distinct("station_id", {"user_id": user["_id"]})
    stations = list(
        db.stations.find(
            {"genres": {"$in": favorite_genres}, "_id": {"$nin": listened_station_ids}},
            {"name": 1, "genres": 1, "country": 1, "city": 1, "rating": 1},
        )
        .sort("rating.average", -1)
        .limit(5)
    )
    tracks = list(
        db.tracks.find(
            {"genre": {"$in": favorite_genres}},
            {"title": 1, "artist": 1, "genre": 1, "popularity": 1, "tags": 1},
        )
        .sort("popularity", -1)
        .limit(5)
    )
    return {"user": user["display_name"], "favorite_genres": favorite_genres, "stations": stations, "tracks": tracks}


def peak_hours(db, station="Jazz Horizon"):
    station_doc = db.stations.find_one({"name": station})
    if not station_doc:
        return {"error": "Station introuvable"}
    return list(
        db.listening_events.aggregate(
            [
                {"$match": {"station_id": station_doc["_id"]}},
                {"$group": {"_id": {"$hour": "$started_at"}, "sessions": {"$sum": 1}, "total_seconds": {"$sum": "$duration_seconds"}}},
                {"$project": {"_id": 0, "hour": "$_id", "sessions": 1, "total_minutes": {"$divide": ["$total_seconds", 60]}}},
                {"$sort": {"total_minutes": -1}},
            ]
        )
    )


def audience_by_city(db, days="30"):
    since = now_utc() - timedelta(days=as_int(days, 30))
    return list(
        db.listening_events.aggregate(
            [
                {"$match": {"started_at": {"$gte": since}}},
                {
                    "$group": {
                        "_id": {"city": "$location.city", "country": "$location.country"},
                        "sessions": {"$sum": 1},
                        "listeners": {"$addToSet": "$user_id"},
                        "total_seconds": {"$sum": "$duration_seconds"},
                    }
                },
                {"$project": {"_id": 0, "city": "$_id.city", "country": "$_id.country", "sessions": 1, "active_listeners": {"$size": "$listeners"}, "total_minutes": {"$divide": ["$total_seconds", 60]}}},
                {"$sort": {"active_listeners": -1, "total_minutes": -1}},
            ]
        )
    )


def user_history(db, email="alice@example.com", limit="10"):
    user = db.users.find_one({"email": email})
    if not user:
        return {"error": "Utilisateur introuvable"}
    return list(
        db.listening_events.aggregate(
            [
                {"$match": {"user_id": user["_id"]}},
                {"$sort": {"started_at": -1}},
                {"$limit": as_int(limit, 10)},
                {"$lookup": {"from": "stations", "localField": "station_id", "foreignField": "_id", "as": "station"}},
                {"$lookup": {"from": "tracks", "localField": "track_id", "foreignField": "_id", "as": "track"}},
                {"$unwind": "$station"},
                {"$unwind": "$track"},
                {"$project": {"_id": 0, "started_at": 1, "duration_seconds": 1, "liked": 1, "device": 1, "station": "$station.name", "track": "$track.title", "artist": "$track.artist"}},
            ]
        )
    )


def playlist_tags(db, limit="8"):
    return list(
        db.playlists.aggregate(
            [
                {"$match": {"visibility": "public"}},
                {"$unwind": "$tags"},
                {"$group": {"_id": "$tags", "playlists": {"$sum": 1}}},
                {"$project": {"_id": 0, "tag": "$_id", "playlists": 1}},
                {"$sort": {"playlists": -1, "tag": 1}},
                {"$limit": as_int(limit, 8)},
            ]
        )
    )


def programs_on_air(db, day="monday", time="08:30"):
    normalized_day = day.lower()
    stations = db.stations.find(
        {"weekly_schedule": {"$elemMatch": {"day": normalized_day, "start": {"$lte": time}, "end": {"$gt": time}}}},
        {"name": 1, "country": 1, "city": 1, "weekly_schedule": 1},
    ).sort("name", 1)
    results = []
    for station in stations:
        station["weekly_schedule"] = [
            program
            for program in station.get("weekly_schedule", [])
            if program["day"] == normalized_day and program["start"] <= time < program["end"]
        ]
        results.append(station)
    return results


def nearby_stations(db, lat="48.8566", lng="2.3522", max_km="900"):
    latitude = as_float(lat, 48.8566)
    longitude = as_float(lng, 2.3522)
    max_meters = as_float(max_km, 900) * 1000
    try:
        return list(
            db.stations.find(
                {
                    "location": {
                        "$near": {
                            "$geometry": {"type": "Point", "coordinates": [longitude, latitude]},
                            "$maxDistance": max_meters,
                        }
                    }
                },
                {"name": 1, "country": 1, "city": 1, "genres": 1, "location": 1},
            ).limit(10)
        )
    except Exception:
        # Fallback useful for local tests with MongoDB mocks that do not implement $near.
        stations = list(db.stations.find({}, {"name": 1, "country": 1, "city": 1, "genres": 1, "location": 1}))
        for station in stations:
            lng2, lat2 = station["location"]["coordinates"]
            station["distance_score"] = (radians(latitude - lat2) ** 2 + radians(longitude - lng2) ** 2) ** 0.5
        return sorted(stations, key=lambda item: item["distance_score"])[:10]


def subscription_segments(db):
    return list(
        db.users.aggregate(
            [
                {"$unwind": "$preferences.favorite_genres"},
                {
                    "$group": {
                        "_id": {
                            "plan": "$subscription.plan",
                            "age_group": "$profile.age_group",
                            "favorite_genre": "$preferences.favorite_genres",
                        },
                        "users": {"$sum": 1},
                    }
                },
                {"$project": {"_id": 0, "plan": "$_id.plan", "age_group": "$_id.age_group", "favorite_genre": "$_id.favorite_genre", "users": 1}},
                {"$sort": {"plan": 1, "age_group": 1, "favorite_genre": 1}},
            ]
        )
    )


def track_retention(db, limit="8"):
    return list(
        db.listening_events.aggregate(
            [
                {"$lookup": {"from": "tracks", "localField": "track_id", "foreignField": "_id", "as": "track"}},
                {"$unwind": "$track"},
                {
                    "$project": {
                        "track_id": 1,
                        "title": "$track.title",
                        "artist": "$track.artist",
                        "duration_seconds": "$track.duration_seconds",
                        "completion_rate": {"$divide": ["$duration_seconds", "$track.duration_seconds"]},
                    }
                },
                {"$group": {"_id": "$track_id", "title": {"$first": "$title"}, "artist": {"$first": "$artist"}, "avg_completion": {"$avg": "$completion_rate"}, "sessions": {"$sum": 1}}},
                {"$project": {"_id": 0, "title": 1, "artist": 1, "sessions": 1, "avg_completion_percent": {"$multiply": ["$avg_completion", 100]}}},
                {"$sort": {"avg_completion_percent": -1, "sessions": -1}},
                {"$limit": as_int(limit, 8)},
            ]
        )
    )


QUERY_FUNCTIONS = {
    "stations_by_genre": stations_by_genre,
    "top_stations": top_stations,
    "liked_tracks_by_genre": liked_tracks_by_genre,
    "personalized_recommendations": personalized_recommendations,
    "peak_hours": peak_hours,
    "audience_by_city": audience_by_city,
    "user_history": user_history,
    "playlist_tags": playlist_tags,
    "programs_on_air": programs_on_air,
    "nearby_stations": nearby_stations,
    "subscription_segments": subscription_segments,
    "track_retention": track_retention,
}
