from flask import Blueprint, jsonify
from app.db.mongo import get_db

health_bp = Blueprint("health", __name__)

@health_bp.route("/", methods=["GET"])
def health_check():
    db = get_db()
    db.command("ping")
    return jsonify({
        "status": "ok",
        "message": "AURONOX backend is running with MongoDB Atlas."
    }), 200