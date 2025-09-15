from flask import Blueprint, request, jsonify
from models import Orders, Wants, Owns, Products, Supermarkets, Users
from database import db

orders_bp = Blueprint('orders', __name__)


@orders_bp.route("/orders", methods=["POST"])
def add_order():
    """
    Create a new order:
    - Receive user_id and product_id from request body
    - Find the wanted quantity from Wants
    - Find the first supermarket (Owns) that has enough stock
    - Create an order linking user, product, and supermarket
    """
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    print(f"Received data: {user_id}, {product_id}")

    if not user_id or not product_id:
        return jsonify({"error": "Fields 'user_id' and 'product_id' are required."}), 400

    wants = Wants.query.filter_by(user_id=user_id, products_id=product_id).first()
    if not wants:
        return jsonify({"error": "No wants found for this user and product."}), 404

    wanted_quantity = wants.quantity

    owns = Owns.query.filter_by(products_id=product_id).filter(Owns.quantity >= wanted_quantity).first()
    if not owns:
        return jsonify({"error": "No supermarket has enough stock for this product."}), 404

    order = Orders(
        user_id=user_id,
        supermarket_id=owns.market_id,
        product_id=product_id,
        order_quantity=wanted_quantity  # <-- set quantity from Wants
    )
    db.session.add(order)

    owns.quantity -= wanted_quantity

    db.session.commit()

    return jsonify({
        "message": "Order created successfully.",
        "order_id": order.id,
        "user_id": user_id,
        "product_id": product_id,
        "supermarket_id": owns.market_id,
        "order_quantity": wanted_quantity
    }), 201


@orders_bp.route("/orders/<int:user_id>", methods=["GET"])
def get_user_orders(user_id):
    """
    Retrieve all orders for a given user.
    """
    orders = Orders.query.filter_by(user_id=user_id).all()
    if not orders:
        return jsonify([]), 200

    orders_data = []
    for order in orders:
        product = Products.query.get(order.product_id)
        supermarket = Supermarkets.query.get(order.supermarket_id)

        orders_data.append({
            "order_id": order.id,
            "product_id": product.id,
            "product_name": product.name,
            "supermarket_id": supermarket.id,
            "supermarket_name": supermarket.name,
            "quantity": order.order_quantity  # <-- use order_quantity
        })

    return jsonify(orders_data), 200


@orders_bp.route("/supermarket_orders/<int:supermarket_id>", methods=["GET"])
def get_supermarket_orders(supermarket_id):
    """
    Retrieve all orders assigned to a given supermarket.
    """
    orders = Orders.query.filter_by(supermarket_id=supermarket_id).all()
    if not orders:
        return jsonify([]), 200

    orders_data = []
    for order in orders:
        product = Products.query.get(order.product_id)
        user = Users.query.get(order.user_id)

        orders_data.append({
            "order_id": order.id,
            "product_id": product.id,
            "product_name": product.name,
            "user_id": user.id,
            "user_name": user.username if user else None,
            "quantity": order.order_quantity  
        })

    return jsonify(orders_data), 200


@orders_bp.route("/supermarket_orders/grouped/<int:supermarket_id>", methods=["GET"])
def get_supermarket_orders_grouped_by_user(supermarket_id):
    """
    Retrieve all orders assigned to a given supermarket, grouped by user_id.
    """
    orders = Orders.query.filter_by(supermarket_id=supermarket_id).all()
    if not orders:
        return jsonify({}), 200

    grouped_orders = {}

    for order in orders:
        product = Products.query.get(order.product_id)
        user = Users.query.get(order.user_id)

        order_data = {
            "order_id": order.id,
            "product_id": product.id,
            "product_name": product.name,
            "quantity": order.order_quantity  
        }

        if order.user_id not in grouped_orders:
            grouped_orders[order.user_id] = []
        grouped_orders[order.user_id].append(order_data)

    return jsonify(grouped_orders), 200

