import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "auronox-secret-key")

    MONGO_URI = os.getenv("MONGO_URI")
    DB_NAME = os.getenv("DB_NAME", "auronox_db")

    # ✅ production frontend (Vercel)
    FRONTEND_ORIGIN = os.getenv(
        "FRONTEND_ORIGIN",
        "https://auronox.vercel.app"
    )
