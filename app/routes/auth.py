from flask import Blueprint, request, jsonify
import hashlib
import hmac
import time
import jwt
from app import app, db, bcrypt
from app.utils import validate_telegram_auth

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Secure Login with Telegram
@bp.route("/login", methods=["POST"])
def login():
    data = request.json
    if not validate_telegram_auth(data):
        return jsonify({"error": "Invalid Telegram authentication"}), 403

    user_id = data["id"]
    user = db.users.find_one({"user_id": user_id})

    if not user:
        user = {
            "user_id": user_id,
            "username": data["username"],
            "first_name": data.get("first_name", ""),
            "last_name": data.get("last_name", ""),
            "profile_photo": data.get("photo_url", ""),
            "created_at": time.time(),
        }
        db.users.insert_one(user)

    # Generate JWT token
    token = jwt.encode({"user_id": user_id, "exp": time.time() + 3600}, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token, "user": user})
