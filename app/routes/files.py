from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from app import app, db

bp = Blueprint("files", __name__, url_prefix="/files")

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "mp4", "mp3"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload a file
@bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    file_data = {
        "filename": filename,
        "url": f"/uploads/{filename}",
        "uploaded_at": time.time(),
    }
    db.files.insert_one(file_data)

    return jsonify({"message": "File uploaded successfully", "url": file_data["url"]})

# List uploaded files
@bp.route("/list", methods=["GET"])
def list_files():
    files = list(db.files.find({}, {"_id": 0}))
    return jsonify({"files": files})
