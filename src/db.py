from pymongo import ASCENDING, GEOSPHERE, MongoClient

from src.config import MONGO_DB, MONGO_URI

_client = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    return _client


def get_db():
    return get_client()[MONGO_DB]


def ensure_indexes(db):
    db.users.create_index("email", unique=True)
    db.users.create_index("preferences.favorite_genres")
    db.stations.create_index("genres")
    db.stations.create_index([("location", GEOSPHERE)])
    db.tracks.create_index([("title", "text"), ("artist", "text"), ("tags", "text")])
    db.tracks.create_index("genre")
    db.listening_events.create_index([("started_at", ASCENDING)])
    db.listening_events.create_index([("station_id", ASCENDING), ("started_at", ASCENDING)])
    db.listening_events.create_index([("user_id", ASCENDING), ("started_at", ASCENDING)])
    db.playlists.create_index("user_id")
    db.playlists.create_index("tags")
