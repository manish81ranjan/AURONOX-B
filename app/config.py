import os
from dotenv import load_dotenv

load_dotenv()
const API_BASE = import.meta.env.VITE_API_BASE;

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "auronox-secret-key")
    MONGO_URI = os.getenv("MONGO_URI", "")
    DB_NAME = os.getenv("DB_NAME", "auronox_db")
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5501")
