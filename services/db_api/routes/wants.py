from flask import Blueprint, request, jsonify
from models import Products, Users, Wants
from database import db

wants_bp = Blueprint('wants', __name__)

@wants_bp.route("/wants", methods=["POST"])
def add_wanting():
    data = request.get_json()

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1) 

    if not user_id or not product_id:
        return jsonify({"error": "Fields 'user_id' and 'product_id' are required."}), 400
    if quantity <= 0:
        return jsonify({"error": "Quantity must be greater than 0."}), 400

    existing_want = Wants.query.filter_by(user_id=user_id, products_id=product_id).first()
    if existing_want:
        return jsonify({
            "message": "Product already in wants. No changes made.",
            "user_id": user_id,
            "product_id": product_id,
            "quantity": existing_want.quantity
        }), 200


    new_want = Wants(user_id=user_id, products_id=product_id, quantity=quantity)
    db.session.add(new_want)
    db.session.commit()

    return jsonify({
        "message": "Product added to wants.",
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity
    }), 201



@wants_bp.route("/wants/<int:user_id>", methods=["GET"])
def get_wanted_products(user_id):
    """Retrieve all products wanted by a specific user."""
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    wanted_products = Wants.query.filter_by(user_id=user_id).all()

    products_data = []
    for want in wanted_products:
        product = Products.query.get(want.products_id)
        if product:
            products_data.append({
                "product_id": product.id,
                "name": product.name,
                "weight": product.weight,
                "photo": product.photo,
                "description": product.description,
                "quantity": want.quantity
            })

    return jsonify(products_data), 200


@wants_bp.route("/wants", methods=["PUT"])
def update_wanted_quantity():
    data = request.get_json()

    user_id = data.get("user_id")
    product_id = data.get("product_id")
    new_quantity = data.get("quantity")

    print(f"Received data: {user_id}, {product_id}, {new_quantity}")

    if not user_id or not product_id or new_quantity is None:
        return jsonify({"error": "Fields 'user_id', 'product_id', and 'quantity' are required."}), 400

    wants = Wants.query.filter_by(user_id=user_id, products_id=product_id).first()
    if not wants:
        return jsonify({"error": "Wants relationship not found for the given user and product."}), 404

    wants.quantity = new_quantity
    db.session.commit()

    return jsonify({"message": "Quantity updated successfully.", "user_id": user_id, "product_id": product_id, "quantity": new_quantity}), 200


@wants_bp.route("/wants/remove", methods=["POST"])
def remove_wanting():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    if not user_id or not product_id:
        return jsonify({"error": "Fields 'user_id' and 'product_id' are required."}), 400

    want = Wants.query.filter_by(user_id=user_id, products_id=product_id).first()
    if not want:
        return jsonify({"error": "Product not found in wants"}), 404

    db.session.delete(want)
    db.session.commit()

    return jsonify({"message": "Product removed from wants"}), 200
