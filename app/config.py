import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://chand37880:4vMXUSi2MyoVd3FY@cluster0.gegvaeq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    TELEGRAM_BOT_TOKEN = os.getenv("3")
