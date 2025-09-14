from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import Products, Like
from database import db

from  models import *

owns_bp = Blueprint('owns', __name__)

@owns_bp.route("/owns", methods=["POST"])
def add_owning():
    data = request.get_json()

    market_id = data.get("supermarket_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    print(product_id, quantity, market_id)
    own = Owns(market_id=market_id, products_id=product_id, quantity=quantity)


    db.session.add(own)
    db.session.commit()

    return {"message": "Product and ownership created"}, 201


@owns_bp.route("/owns/<int:supermarket_id>", methods=["GET"])
def get_owned_products(supermarket_id):
    supermarket = Supermarkets.query.get(supermarket_id)
    if not supermarket:
        return jsonify({"error": "Supermarket not found"}), 404

    owned_products = Owns.query.filter_by(market_id=supermarket_id).all()

    products_data = []
    for ownership in owned_products:
        product = Products.query.get(ownership.products_id)
        if product:
            products_data.append({
                "id": product.id,
                "name": product.name,
                "weight": product.weight,
                "photo": product.photo,
                "description": product.description,
                "quantity": ownership.quantity
            })

    return jsonify(products_data), 200


@owns_bp.route("/owns", methods=["PUT"])
def update_owned_quantity():
    """Update the quantity of a product owned by a supermarket."""
    data = request.get_json()

    supermarket_id = data.get("supermarket_id")
    product_id = data.get("product_id")
    new_quantity = data.get("quantity")

    if not supermarket_id or not product_id or new_quantity is None:
        return jsonify({"error": "Fields 'supermarket_id', 'product_id', and 'quantity' are required."}), 400

    ownership = Owns.query.filter_by(market_id=supermarket_id, products_id=product_id).first()
    if not ownership:
        return jsonify({"error": "Ownership relationship not found for the given supermarket and product."}), 404

    ownership.quantity = new_quantity
    db.session.commit()

    return jsonify({
        "message": "Quantity updated successfully.",
        "supermarket_id": supermarket_id,
        "product_id": product_id,
        "quantity": new_quantity
    }), 200