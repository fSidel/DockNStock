from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import Products, Like
from database import db

from  models import *

like_bp = Blueprint('like', __name__)

@like_bp.route("/like/<int:user_id>/<int:product_id>", methods=["POST"])
def toggle_like(user_id, product_id):
    # Check if user and product exist
    user = Users.query.get(user_id)
    product = Products.query.get(product_id)

    if not user or not product:
        return jsonify({"error": "User or Product not found"}), 404

    # Check if the like already exists
    like = Like.query.filter_by(users_id=user_id, products_id=product_id).first()
    
    if like:
        # Remove existing like
        db.session.delete(like)
        db.session.commit()
        return jsonify({"message": "Like removed"}), 201
    else:
        # Add new like
        new_like = Like(users_id=user_id, products_id=product_id)
        db.session.add(new_like)
        db.session.commit()
        return jsonify({"message": "Like added"}), 200
