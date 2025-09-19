from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import Products, Users
from database import db

from  models import *

comment_bp = Blueprint('comment', __name__)

@comment_bp.route("/comment", methods=["POST"])
def create_comment():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    msg_sent = data.get("comment")

    # Check required fields
    if not user_id or not product_id or not msg_sent:
        return jsonify({"error": "user_id, product_id and comment are required"}), 400

    # Check if user and product exist
    user = Users.query.get(user_id)
    product = Products.query.get(product_id)

    if not user or not product:
        return jsonify({"error": "User or Product not found"}), 404

    # Create and save new comment
    new_comment = Comments(users_id=user_id, products_id=product_id, comment=msg_sent)
    db.session.add(new_comment)
    db.session.commit()

    user = Users.query.get(user_id)

    return jsonify({
        "user": user.to_dict()
    }), 200

@comment_bp.route("/get_comments", methods=["GET"])
def get_all_comments():
    comments = Comments.query.all()

    results = []
    for c in comments:
        results.append({
            "comment_id": c.id,
            "comment": c.comment,
            "user": c.users_comments.to_dict(),
            "product": c.product_has_comments.to_dict()
        })

    return jsonify(results), 200

@comment_bp.route("/user_comment/<int:user_id>", methods=["GET"])
def get_comments_by_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    comments = Comments.query.filter_by(users_id=user_id).all()

    results = []
    for c in comments:
        results.append({
            "comment": c.comment,
            # "product": c.product_has_comments.to_dict()
        })

    return jsonify(results), 200

@comment_bp.route("/product_comments/<int:product_id>", methods=["GET"])
def get_comments_by_product(product_id):
    product = Products.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    comments = Comments.query.filter_by(products_id=product_id).all()

    results = []
    for c in comments:
        results.append({
            "comment_id": c.id,
            "comment": c.comment,
            "user": c.users_comments.to_dict(),
        })

    return jsonify(results), 200


