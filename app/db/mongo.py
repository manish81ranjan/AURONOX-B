from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = None
db = None


def init_mongo(app):
    global client, db

    mongo_uri = app.config.get("MONGO_URI")
    db_name = app.config.get("DB_NAME", "auronox_db")

    if not mongo_uri:
        raise ValueError("❌ MONGO_URI is missing in .env")

    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]

        # ✅ Test connection
        client.admin.command("ping")
        print("✅ MongoDB Connected Successfully")

        # =========================
        # 🔥 COLLECTION INDEXES
        # =========================

        # Products
        db.products.create_index("id", unique=True)

        # Orders
        db.orders.create_index("order_id", unique=True)

        # Users (AUTH)
        db.users.create_index("email", unique=True)

        # Optional indexes (performance)
        db.products.create_index("category")
        db.products.create_index("series")

        print("✅ MongoDB Indexes Created")

    except ConnectionFailure:
        raise RuntimeError("❌ MongoDB Connection Failed")


def get_db():
    global db

    if db is None:
        raise RuntimeError("❌ MongoDB is not initialized. Call init_mongo() first.")

    return db