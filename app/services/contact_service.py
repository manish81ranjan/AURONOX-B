from app.db.mongo import get_db
from datetime import datetime

def save_contact(payload):
    db = get_db()

    doc = {
        "name": payload.get("name"),
        "email": payload.get("email"),
        "subject": payload.get("subject"),
        "message": payload.get("message"),
        "created_at": datetime.utcnow().isoformat()
    }

    db.contacts.insert_one(doc)
    doc.pop("_id", None)
    return doc