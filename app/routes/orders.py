from flask import Blueprint, jsonify, request
from app.services.order_service import create_order, get_all_orders

orders_bp = Blueprint("orders", __name__)

@orders_bp.route("/", methods=["GET"])
def fetch_orders():
    orders = get_all_orders()
    return jsonify(orders), 200

@orders_bp.route("/", methods=["POST"])
def place_order():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "firstName", "lastName", "email", "phone",
        "address", "city", "state", "pinCode", "paymentMethod"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required."}), 400

    order = create_order(data)
    return jsonify({
        "message": "Order placed successfully.",
        "order": order
    }), 201