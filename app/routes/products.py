from flask import Blueprint, jsonify, request
from app.services.product_service import (
    seed_products_if_empty,
    get_all_products,
    get_product_by_id
)

products_bp = Blueprint("products", __name__)

@products_bp.route("/seed", methods=["POST"])
def seed_products():
    seed_products_if_empty()
    return jsonify({"message": "Products seeded successfully."}), 201

@products_bp.route("/", methods=["GET"])
def fetch_products():
    category = request.args.get("category")
    products = get_all_products(category)
    return jsonify(products), 200

@products_bp.route("/<product_id>", methods=["GET"])
def fetch_product(product_id):
    product = get_product_by_id(product_id)

    if not product:
        return jsonify({"message": "Product not found."}), 404

    return jsonify(product), 200