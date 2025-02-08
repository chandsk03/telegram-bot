from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from app.config import Config

# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)

# Security & CORS
CORS(app)
bcrypt = Bcrypt(app)

# MongoDB Setup
mongo = MongoClient(app.config["MONGO_URI"])
db = mongo.get_database("telegram_mini_app")

# WebSockets
socketio = SocketIO(app, cors_allowed_origins="*")

# Import Routes
from app.routes import auth, chat, files

app.register_blueprint(auth.bp)
app.register_blueprint(chat.bp)
app.register_blueprint(files.bp)
