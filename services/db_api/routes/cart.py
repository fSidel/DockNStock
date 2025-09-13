from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import Products, Like
from database import db

from  models import *

cart_bp = Blueprint('cart', __name__)

@cart_bp.route("/cart", methods=["POST"])
def adds_to_cart():
    # Check if user and product exist
    data = request.json
    user_id = data["user_id"]
    product_id = data["product_id"]
    user = Users.query.get(user_id)
    product = Products.query.get(product_id)

    if not user or not product:
        return jsonify({"error": "User or Product not found"}), 404

    # Check if the cart already exists
    cart = Cart.query.filter_by(users_id=user_id, products_id=product_id).first()
    
    if cart:
        # Remove existing cart
        db.session.delete(cart)
        db.session.commit()
        return jsonify({"message": "Like removed"}), 201
    else:
        # Add new cart
        new_cart = Cart(users_id=user_id, products_id=product_id)
        db.session.add(new_cart)
        db.session.commit()
        return jsonify({"message": "Like added"}), 200


@cart_bp.route("/cart/<int:user_id>", methods=["GET"])
def get_cart(user_id):
    # Check if the user exists
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve all products in the user's cart
    cart_items = Cart.query.filter_by(users_id=user_id).all()
    if not cart_items:
        return jsonify([]), 200 # Return an empty list if the cart is empty

    # Prepare the response
    results = []
    for item in cart_items:
        product = item.product_put_in_cart  # Use the relationship to get the product
        if product:
            results.append({
                "product_id": product.id,
                "name": product.name,
                "weight": product.weight,
                "photo": product.photo,
                "description": product.description
            })
    
    return jsonify(results), 200


@cart_bp.route("/cart/remove", methods=["POST"])
def remove_from_cart():
    # Parse the request data
    data = request.json
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    # Validate user and product
    user = Users.query.get(user_id)
    product = Products.query.get(product_id)

    if not user or not product:
        return jsonify({"error": "User or Product not found"}), 404

    # Check if the product exists in the user's cart
    cart_item = Cart.query.filter_by(users_id=user_id, products_id=product_id).first()
    if not cart_item:
        return jsonify({"error": "Product not found in cart"}), 404

    # Remove the product from the cart
    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Product removed from cart"}), 200


@cart_bp.route("/cart_id/<int:user_id>", methods=["GET"])
def get_cart_id(user_id):
    """Retrieve the cart ID for a given user ID."""
    # Check if the user exists
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Retrieve the cart for the user
    cart = Cart.query.filter_by(users_id=user_id).first()
    if not cart:
        return jsonify({"error": "Cart not found for the user"}), 404

    # Return the cart ID
    return jsonify({"cart_id": cart.id}), 200
