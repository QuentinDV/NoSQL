from datetime import date, datetime
from pathlib import Path

from bson import ObjectId
from flask import Flask, jsonify, request, send_from_directory

from src.db import ensure_indexes, get_db
from src.queries import QUERY_FUNCTIONS, QUERY_REGISTRY

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"


def serialize(value):
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize(item) for key, item in value.items()}
    return value


def create_app():
    app = Flask(__name__, static_folder=None)

    @app.before_request
    def prepare_database():
        ensure_indexes(get_db())

    @app.get("/")
    def index():
        return send_from_directory(WEB_DIR, "index.html")

    @app.get("/web/<path:filename>")
    def web_assets(filename):
        return send_from_directory(WEB_DIR, filename)

    @app.get("/api/health")
    def health():
        db = get_db()
        db.command("ping")
        return jsonify({"status": "ok", "database": db.name})

    @app.get("/api/queries")
    def list_queries():
        return jsonify(QUERY_REGISTRY)

    @app.get("/api/queries/<query_id>")
    def run_query(query_id):
        query = QUERY_FUNCTIONS.get(query_id)
        if not query:
            return jsonify({"error": "Requete inconnue"}), 404
        params = request.args.to_dict()
        result = query(get_db(), **params)
        return jsonify({"query_id": query_id, "params": params, "result": serialize(result)})

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
