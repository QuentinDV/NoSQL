from datetime import datetime, timedelta, timezone
from time import sleep

from bson import ObjectId
from pymongo.errors import ServerSelectionTimeoutError

from src.db import ensure_indexes, get_db


ID = {
    "station_jazz": ObjectId("650000000000000000000001"),
    "station_pop": ObjectId("650000000000000000000002"),
    "station_electro": ObjectId("650000000000000000000003"),
    "station_news": ObjectId("650000000000000000000004"),
    "station_lofi": ObjectId("650000000000000000000005"),
    "station_latina": ObjectId("650000000000000000000006"),
    "track_1": ObjectId("651000000000000000000001"),
    "track_2": ObjectId("651000000000000000000002"),
    "track_3": ObjectId("651000000000000000000003"),
    "track_4": ObjectId("651000000000000000000004"),
    "track_5": ObjectId("651000000000000000000005"),
    "track_6": ObjectId("651000000000000000000006"),
    "track_7": ObjectId("651000000000000000000007"),
    "track_8": ObjectId("651000000000000000000008"),
    "track_9": ObjectId("651000000000000000000009"),
    "track_10": ObjectId("651000000000000000000010"),
    "track_11": ObjectId("651000000000000000000011"),
    "track_12": ObjectId("651000000000000000000012"),
    "user_1": ObjectId("652000000000000000000001"),
    "user_2": ObjectId("652000000000000000000002"),
    "user_3": ObjectId("652000000000000000000003"),
    "user_4": ObjectId("652000000000000000000004"),
    "user_5": ObjectId("652000000000000000000005"),
    "user_6": ObjectId("652000000000000000000006"),
}


def utc_now():
    return datetime.now(timezone.utc).replace(microsecond=0)


def build_stations():
    return [
        {
            "_id": ID["station_jazz"],
            "name": "Jazz Horizon",
            "country": "France",
            "city": "Paris",
            "genres": ["jazz", "soul", "blues"],
            "language": "fr",
            "bitrate_kbps": 192,
            "location": {"type": "Point", "coordinates": [2.3522, 48.8566]},
            "rating": {"average": 4.7, "count": 428},
            "weekly_schedule": [
                {"day": "monday", "start": "08:00", "end": "11:00", "program": "Morning Jazz", "host": "Nora"},
                {"day": "friday", "start": "20:00", "end": "23:00", "program": "Blue Notes", "host": "Samir"},
            ],
        },
        {
            "_id": ID["station_pop"],
            "name": "Pop Pulse",
            "country": "France",
            "city": "Lyon",
            "genres": ["pop", "dance"],
            "language": "fr",
            "bitrate_kbps": 256,
            "location": {"type": "Point", "coordinates": [4.8357, 45.7640]},
            "rating": {"average": 4.4, "count": 810},
            "weekly_schedule": [
                {"day": "monday", "start": "17:00", "end": "20:00", "program": "Hit Drive", "host": "Lina"},
                {"day": "saturday", "start": "18:00", "end": "21:00", "program": "Top 40", "host": "Max"},
            ],
        },
        {
            "_id": ID["station_electro"],
            "name": "ElectroLab",
            "country": "Germany",
            "city": "Berlin",
            "genres": ["electro", "techno", "house"],
            "language": "en",
            "bitrate_kbps": 320,
            "location": {"type": "Point", "coordinates": [13.4050, 52.5200]},
            "rating": {"average": 4.8, "count": 622},
            "weekly_schedule": [
                {"day": "friday", "start": "22:00", "end": "23:59", "program": "Warehouse Live", "host": "Mika"},
                {"day": "saturday", "start": "00:00", "end": "02:00", "program": "Warehouse Live", "host": "Mika"},
            ],
        },
        {
            "_id": ID["station_news"],
            "name": "World Brief",
            "country": "United Kingdom",
            "city": "London",
            "genres": ["news", "business", "culture"],
            "language": "en",
            "bitrate_kbps": 128,
            "location": {"type": "Point", "coordinates": [-0.1276, 51.5072]},
            "rating": {"average": 4.2, "count": 305},
            "weekly_schedule": [
                {"day": "monday", "start": "07:00", "end": "09:00", "program": "Market Open", "host": "Ava"},
                {"day": "wednesday", "start": "12:00", "end": "13:00", "program": "Culture Desk", "host": "Owen"},
            ],
        },
        {
            "_id": ID["station_lofi"],
            "name": "LoFi Campus",
            "country": "France",
            "city": "Nantes",
            "genres": ["lofi", "ambient", "study"],
            "language": "fr",
            "bitrate_kbps": 192,
            "location": {"type": "Point", "coordinates": [-1.5536, 47.2184]},
            "rating": {"average": 4.6, "count": 512},
            "weekly_schedule": [
                {"day": "tuesday", "start": "19:00", "end": "22:00", "program": "Deep Focus", "host": "Iris"},
                {"day": "thursday", "start": "14:00", "end": "17:00", "program": "Soft Study", "host": "Iris"},
            ],
        },
        {
            "_id": ID["station_latina"],
            "name": "Latina Club",
            "country": "Spain",
            "city": "Barcelona",
            "genres": ["latin", "reggaeton", "dance"],
            "language": "es",
            "bitrate_kbps": 256,
            "location": {"type": "Point", "coordinates": [2.1734, 41.3851]},
            "rating": {"average": 4.5, "count": 377},
            "weekly_schedule": [
                {"day": "saturday", "start": "21:00", "end": "23:59", "program": "Fiesta Mix", "host": "Sofia"},
                {"day": "sunday", "start": "16:00", "end": "18:00", "program": "Latina Family", "host": "Mateo"},
            ],
        },
    ]


def build_tracks():
    return [
        {"_id": ID["track_1"], "title": "Blue River", "artist": "Nora Miles", "genre": "jazz", "duration_seconds": 241, "tags": ["saxophone", "night"], "popularity": 92},
        {"_id": ID["track_2"], "title": "Late Station", "artist": "The B-Sides", "genre": "blues", "duration_seconds": 218, "tags": ["guitar", "classic"], "popularity": 74},
        {"_id": ID["track_3"], "title": "City Sparks", "artist": "Luna Wave", "genre": "pop", "duration_seconds": 196, "tags": ["summer", "chorus"], "popularity": 96},
        {"_id": ID["track_4"], "title": "Drive Home", "artist": "Max Vale", "genre": "dance", "duration_seconds": 205, "tags": ["commute", "energy"], "popularity": 88},
        {"_id": ID["track_5"], "title": "Warehouse Signal", "artist": "Mika North", "genre": "techno", "duration_seconds": 389, "tags": ["club", "bass"], "popularity": 95},
        {"_id": ID["track_6"], "title": "Analog Pulse", "artist": "Kraft Point", "genre": "electro", "duration_seconds": 312, "tags": ["synth", "retro"], "popularity": 83},
        {"_id": ID["track_7"], "title": "Market Minute", "artist": "World Brief Desk", "genre": "business", "duration_seconds": 540, "tags": ["news", "finance"], "popularity": 61},
        {"_id": ID["track_8"], "title": "Culture Lens", "artist": "Ava Owen", "genre": "culture", "duration_seconds": 480, "tags": ["interview", "city"], "popularity": 58},
        {"_id": ID["track_9"], "title": "Quiet Notebook", "artist": "Iris Bloom", "genre": "lofi", "duration_seconds": 170, "tags": ["study", "soft"], "popularity": 90},
        {"_id": ID["track_10"], "title": "Rainy Campus", "artist": "LoFi Campus Band", "genre": "ambient", "duration_seconds": 212, "tags": ["rain", "focus"], "popularity": 86},
        {"_id": ID["track_11"], "title": "Barcelona Heat", "artist": "Sofia Cruz", "genre": "latin", "duration_seconds": 224, "tags": ["party", "summer"], "popularity": 89},
        {"_id": ID["track_12"], "title": "Noche Viva", "artist": "Mateo Sol", "genre": "reggaeton", "duration_seconds": 232, "tags": ["dance", "club"], "popularity": 91},
    ]


def build_users():
    return [
        {
            "_id": ID["user_1"],
            "email": "alice@example.com",
            "display_name": "Alice",
            "profile": {"age_group": "18-25", "country": "France", "city": "Paris"},
            "preferences": {"favorite_genres": ["jazz", "lofi"], "languages": ["fr", "en"], "explicit_content": False},
            "subscription": {"plan": "premium", "started_at": utc_now() - timedelta(days=120)},
            "devices": [{"type": "mobile", "os": "iOS"}, {"type": "web", "os": "Windows"}],
        },
        {
            "_id": ID["user_2"],
            "email": "mehdi@example.com",
            "display_name": "Mehdi",
            "profile": {"age_group": "26-35", "country": "France", "city": "Lyon"},
            "preferences": {"favorite_genres": ["pop", "dance"], "languages": ["fr"], "explicit_content": True},
            "subscription": {"plan": "free", "started_at": utc_now() - timedelta(days=40)},
            "devices": [{"type": "mobile", "os": "Android"}],
        },
        {
            "_id": ID["user_3"],
            "email": "emma@example.com",
            "display_name": "Emma",
            "profile": {"age_group": "18-25", "country": "Germany", "city": "Berlin"},
            "preferences": {"favorite_genres": ["electro", "techno"], "languages": ["en"], "explicit_content": True},
            "subscription": {"plan": "premium", "started_at": utc_now() - timedelta(days=300)},
            "devices": [{"type": "desktop", "os": "macOS"}],
        },
        {
            "_id": ID["user_4"],
            "email": "oliver@example.com",
            "display_name": "Oliver",
            "profile": {"age_group": "36-45", "country": "United Kingdom", "city": "London"},
            "preferences": {"favorite_genres": ["news", "business"], "languages": ["en"], "explicit_content": False},
            "subscription": {"plan": "free", "started_at": utc_now() - timedelta(days=15)},
            "devices": [{"type": "web", "os": "Linux"}],
        },
        {
            "_id": ID["user_5"],
            "email": "chloe@example.com",
            "display_name": "Chloe",
            "profile": {"age_group": "18-25", "country": "France", "city": "Nantes"},
            "preferences": {"favorite_genres": ["lofi", "ambient"], "languages": ["fr"], "explicit_content": False},
            "subscription": {"plan": "student", "started_at": utc_now() - timedelta(days=80)},
            "devices": [{"type": "mobile", "os": "Android"}, {"type": "smart_speaker", "os": "HomeOS"}],
        },
        {
            "_id": ID["user_6"],
            "email": "lucia@example.com",
            "display_name": "Lucia",
            "profile": {"age_group": "26-35", "country": "Spain", "city": "Barcelona"},
            "preferences": {"favorite_genres": ["latin", "reggaeton", "dance"], "languages": ["es", "en"], "explicit_content": True},
            "subscription": {"plan": "premium", "started_at": utc_now() - timedelta(days=65)},
            "devices": [{"type": "mobile", "os": "iOS"}],
        },
    ]


def event(user_key, station_key, track_key, days_ago, hour, minute, duration, city, country, liked):
    started = (utc_now() - timedelta(days=days_ago)).replace(hour=hour, minute=minute, second=0)
    return {
        "user_id": ID[user_key],
        "station_id": ID[station_key],
        "track_id": ID[track_key],
        "started_at": started,
        "duration_seconds": duration,
        "device": "mobile" if hour >= 17 else "web",
        "location": {"city": city, "country": country},
        "liked": liked,
    }


def build_events():
    rows = [
        ("user_1", "station_jazz", "track_1", 1, 8, 15, 235, "Paris", "France", True),
        ("user_1", "station_lofi", "track_9", 2, 21, 10, 170, "Paris", "France", True),
        ("user_1", "station_jazz", "track_2", 6, 20, 30, 188, "Paris", "France", False),
        ("user_2", "station_pop", "track_3", 0, 18, 5, 196, "Lyon", "France", True),
        ("user_2", "station_pop", "track_4", 3, 17, 45, 205, "Lyon", "France", True),
        ("user_2", "station_latina", "track_12", 8, 22, 15, 140, "Lyon", "France", False),
        ("user_3", "station_electro", "track_5", 1, 23, 20, 389, "Berlin", "Germany", True),
        ("user_3", "station_electro", "track_6", 4, 0, 30, 300, "Berlin", "Germany", True),
        ("user_3", "station_pop", "track_4", 9, 18, 0, 176, "Berlin", "Germany", False),
        ("user_4", "station_news", "track_7", 0, 7, 30, 520, "London", "United Kingdom", True),
        ("user_4", "station_news", "track_8", 2, 12, 20, 410, "London", "United Kingdom", False),
        ("user_4", "station_jazz", "track_1", 11, 20, 0, 210, "London", "United Kingdom", True),
        ("user_5", "station_lofi", "track_9", 0, 14, 30, 170, "Nantes", "France", True),
        ("user_5", "station_lofi", "track_10", 1, 19, 10, 212, "Nantes", "France", True),
        ("user_5", "station_jazz", "track_1", 7, 8, 20, 200, "Nantes", "France", False),
        ("user_6", "station_latina", "track_11", 1, 21, 5, 224, "Barcelona", "Spain", True),
        ("user_6", "station_latina", "track_12", 3, 22, 10, 232, "Barcelona", "Spain", True),
        ("user_6", "station_pop", "track_3", 12, 18, 40, 196, "Barcelona", "Spain", True),
    ]
    expanded = []
    for index, args in enumerate(rows):
        doc = event(*args)
        doc["_id"] = ObjectId()
        expanded.append(doc)
        if index % 2 == 0:
            duplicate = event(*args[:3], args[3] + 14, args[4], args[5], max(args[6] - 20, 90), args[7], args[8], args[9])
            duplicate["_id"] = ObjectId()
            expanded.append(duplicate)
    return expanded


def build_playlists():
    return [
        {"_id": ObjectId(), "user_id": ID["user_1"], "name": "Jazz pour coder", "visibility": "private", "tags": ["focus", "jazz"], "items": [{"track_id": ID["track_1"], "added_at": utc_now() - timedelta(days=10)}, {"track_id": ID["track_9"], "added_at": utc_now() - timedelta(days=3)}]},
        {"_id": ObjectId(), "user_id": ID["user_2"], "name": "Trajet du soir", "visibility": "public", "tags": ["commute", "pop"], "items": [{"track_id": ID["track_3"], "added_at": utc_now() - timedelta(days=8)}, {"track_id": ID["track_4"], "added_at": utc_now() - timedelta(days=4)}]},
        {"_id": ObjectId(), "user_id": ID["user_3"], "name": "Warehouse", "visibility": "public", "tags": ["club", "techno"], "items": [{"track_id": ID["track_5"], "added_at": utc_now() - timedelta(days=15)}, {"track_id": ID["track_6"], "added_at": utc_now() - timedelta(days=6)}]},
        {"_id": ObjectId(), "user_id": ID["user_5"], "name": "Revision calme", "visibility": "public", "tags": ["study", "focus"], "items": [{"track_id": ID["track_9"], "added_at": utc_now() - timedelta(days=12)}, {"track_id": ID["track_10"], "added_at": utc_now() - timedelta(days=5)}]},
        {"_id": ObjectId(), "user_id": ID["user_6"], "name": "Fiesta", "visibility": "public", "tags": ["party", "dance"], "items": [{"track_id": ID["track_11"], "added_at": utc_now() - timedelta(days=14)}, {"track_id": ID["track_12"], "added_at": utc_now() - timedelta(days=7)}]},
    ]


def wait_for_mongo(db, attempts=20):
    for attempt in range(1, attempts + 1):
        try:
            db.command("ping")
            return
        except ServerSelectionTimeoutError:
            if attempt == attempts:
                raise
            sleep(1)


def seed_database():
    db = get_db()
    wait_for_mongo(db)
    ensure_indexes(db)
    for collection in ["stations", "tracks", "users", "listening_events", "playlists"]:
        db[collection].delete_many({})
    db.stations.insert_many(build_stations())
    db.tracks.insert_many(build_tracks())
    db.users.insert_many(build_users())
    db.listening_events.insert_many(build_events())
    db.playlists.insert_many(build_playlists())
    return {
        "stations": db.stations.count_documents({}),
        "tracks": db.tracks.count_documents({}),
        "users": db.users.count_documents({}),
        "listening_events": db.listening_events.count_documents({}),
        "playlists": db.playlists.count_documents({}),
    }


if __name__ == "__main__":
    print(seed_database())
