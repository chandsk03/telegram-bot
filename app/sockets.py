from app import socketio, db
from flask_socketio import emit, join_room, leave_room

@socketio.on("join")
def handle_join(data):
    user_id = data["user_id"]
    room_id = data["room_id"]
    join_room(room_id)
    emit("user_joined", {"user_id": user_id}, room=room_id)

@socketio.on("message")
def handle_message(data):
    user_id = data["user_id"]
    room_id = data["room_id"]
    message = data["message"]

    chat_message = {
        "user_id": user_id,
        "room_id": room_id,
        "message": message,
        "timestamp": time.time()
    }

    db.messages.insert_one(chat_message)
    emit("new_message", chat_message, room=room_id)

@socketio.on("leave")
def handle_leave(data):
    user_id = data["user_id"]
    room_id = data["room_id"]
    leave_room(room_id)
    emit("user_left", {"user_id": user_id}, room=room_id)
