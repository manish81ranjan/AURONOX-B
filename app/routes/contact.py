from flask import Blueprint, jsonify, request
from app.services.contact_service import save_contact

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/", methods=["POST"])
def submit_contact():
    data = request.get_json(silent=True) or {}

    required_fields = ["name", "email", "subject", "message"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required."}), 400

    contact = save_contact(data)
    return jsonify({
        "message": "Contact request submitted successfully.",
        "contact": contact
    }), 201