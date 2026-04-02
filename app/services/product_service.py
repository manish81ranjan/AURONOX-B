from app.db.mongo import get_db
from app.data.catalog import CATALOG

def seed_products_if_empty():
    db = get_db()
    count = db.products.count_documents({})

    if count == 0:
        db.products.insert_many(CATALOG)

def get_all_products(category=None):
    db = get_db()
    query = {}

    if category and category != "all":
        query["category"] = category

    products = list(db.products.find(query, {"_id": 0}))
    return products

def get_product_by_id(product_id):
    db = get_db()
    return db.products.find_one({"id": product_id}, {"_id": 0})