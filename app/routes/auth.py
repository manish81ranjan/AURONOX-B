from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt

from app.db.mongo import get_db

auth_bp = Blueprint("auth", __name__)


def create_token(user_id, email):
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")


def get_token_user():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1].strip()

    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload
    except Exception:
        return None


@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db()
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not name or not email or not password:
        return jsonify({"message": "All fields are required."}), 400

    if len(password) < 6:
        return jsonify({"message": "Password must be at least 6 characters."}), 400

    existing = db.users.find_one({"email": email})
    if existing:
        return jsonify({"message": "Email already registered."}), 409

    user_doc = {
        "name": name,
        "email": email,
        "password_hash": generate_password_hash(password),
        "created_at": datetime.utcnow().strftime("%d %b %Y")
    }

    result = db.users.insert_one(user_doc)

    token = create_token(result.inserted_id, email)

    return jsonify({
        "message": "Account created successfully.",
        "token": token,
        "user": {
            "id": str(result.inserted_id),
            "name": name,
            "email": email,
            "created_at": user_doc["created_at"]
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db()
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()

    if not email or not password:
        return jsonify({"message": "Email and password are required."}), 400

    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({"message": "Invalid email or password."}), 401

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"message": "Invalid email or password."}), 401

    token = create_token(user["_id"], user["email"])

    return jsonify({
        "message": "Login successful.",
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "created_at": user.get("created_at", "")
        }
    }), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    db = get_db()
    payload = get_token_user()

    if not payload:
        return jsonify({"message": "Unauthorized."}), 401

    email = payload.get("email")
    user = db.users.find_one({"email": email})

    if not user:
        return jsonify({"message": "User not found."}), 404

    return jsonify({
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "created_at": user.get("created_at", "")
        }
    }), 200