import mongomock

from src.queries import QUERY_FUNCTIONS
from src.seed import build_events, build_playlists, build_stations, build_tracks, build_users


def build_db():
    client = mongomock.MongoClient()
    db = client.radiostream_test
    db.stations.insert_many(build_stations())
    db.tracks.insert_many(build_tracks())
    db.users.insert_many(build_users())
    db.listening_events.insert_many(build_events())
    db.playlists.insert_many(build_playlists())
    return db


def test_all_registered_queries_return_data():
    db = build_db()
    for query_id, query in QUERY_FUNCTIONS.items():
        result = query(db)
        assert result is not None, query_id


def test_personalized_recommendations_have_tracks():
    db = build_db()
    result = QUERY_FUNCTIONS["personalized_recommendations"](db, email="alice@example.com")
    assert result["user"] == "Alice"
    assert result["tracks"]


def test_stations_by_genre_filters_genre():
    db = build_db()
    result = QUERY_FUNCTIONS["stations_by_genre"](db, genre="jazz")
    assert result
    assert all("jazz" in station["genres"] for station in result)
