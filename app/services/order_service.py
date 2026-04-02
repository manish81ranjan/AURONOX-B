from app.db.mongo import get_db
from datetime import datetime
import random

def generate_order_id():
    return f"ORD-{random.randint(100000, 999999)}"

def create_order(payload):
    db = get_db()

    order = {
        "order_id": generate_order_id(),
        "customer": {
            "first_name": payload.get("firstName"),
            "last_name": payload.get("lastName"),
            "email": payload.get("email"),
            "phone": payload.get("phone"),
            "address": payload.get("address"),
            "city": payload.get("city"),
            "state": payload.get("state"),
            "pin_code": payload.get("pinCode"),
        },
        "payment_method": payload.get("paymentMethod"),
        "items": payload.get("items", []),
        "subtotal": payload.get("subtotal", 0),
        "total": payload.get("total", 0),
        "status": "Confirmed",
        "created_at": datetime.utcnow().isoformat()
    }

    db.orders.insert_one(order)
    order.pop("_id", None)
    return order

def get_all_orders():
    db = get_db()
    return list(db.orders.find({}, {"_id": 0}).sort("created_at", -1))