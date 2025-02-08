from flask import Blueprint, request, jsonify
from app import db
import time
import uuid

bp = Blueprint("chat", __name__, url_prefix="/chat")

# Create a new chat room
@bp.route("/create", methods=["POST"])
def create_room():
    data = request.json
    user_id = data["user_id"]
    room_name = data["room_name"]

    room_id = str(uuid.uuid4())
    room = {
        "room_id": room_id,
        "room_name": room_name,
        "owner": user_id,
        "members": [user_id],
        "created_at": time.time()
    }
    db.rooms.insert_one(room)

    return jsonify({"room_id": room_id, "room_name": room_name})

# Join a chat room
@bp.route("/join", methods=["POST"])
def join_room():
    data = request.json
    user_id = data["user_id"]
    room_id = data["room_id"]

    room = db.rooms.find_one({"room_id": room_id})
    if not room:
        return jsonify({"error": "Room not found"}), 404

    if user_id not in room["members"]:
        db.rooms.update_one({"room_id": room_id}, {"$push": {"members": user_id}})

    return jsonify({"message": "Joined successfully"})

# List all chat rooms
@bp.route("/list", methods=["GET"])
def list_rooms():
    rooms = list(db.rooms.find({}, {"_id": 0}))
    return jsonify({"rooms": rooms})

# Delete a chat room
@bp.route("/delete", methods=["POST"])
def delete_room():
    data = request.json
    user_id = data["user_id"]
    room_id = data["room_id"]

    room = db.rooms.find_one({"room_id": room_id})
    if not room or room["owner"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.rooms.delete_one({"room_id": room_id})
    return jsonify({"message": "Room deleted successfully"})
