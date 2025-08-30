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

    # Check if the like already exists
    cart = Cart.query.filter_by(users_id=user_id, products_id=product_id).first()
    
    if cart:
        # Remove existing like
        db.session.delete(cart)
        db.session.commit()
        return jsonify({"message": "Like removed"}), 201
    else:
        # Add new like
        new_cart = Cart(users_id=user_id, products_id=product_id)
        db.session.add(new_cart)
        db.session.commit()
        return jsonify({"message": "Like added"}), 200
