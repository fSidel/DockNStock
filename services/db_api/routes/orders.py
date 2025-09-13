from flask import Blueprint, request, jsonify
from models import Orders, Cart, Products, Supermarkets
from database import db

orders_bp = Blueprint('orders', __name__)


""" orders_bp.route('/create_order', methods=['POST'])
def create_order():
    data = request.json  # Get the JSON payload

    # Validate the incoming data
    cart_id = data.get("cart_id")
    supermarket_id = data.get("supermarket_id")
    tracking_code = data.get("tracking_code")

    if not cart_id or not supermarket_id or not tracking_code:
        return jsonify({"error": "Fields 'cart_id', 'supermarket_id', and 'tracking_code' are required."}), 400

    # Retrieve the cart from the database
    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({"error": f"Cart with ID {cart_id} does not exist."}), 404

    # Ensure the tracking code matches the cart's tracking code
    if cart.tracking_code != tracking_code:
        return jsonify({"error": "Tracking code does not match the cart's tracking code."}), 400

    # Create the order
    try:
        new_order = Orders(cart=cart, supermarket_id=supermarket_id)
        db.session.add(new_order)

        # Delete the cart after successfully creating the order
        db.session.delete(cart)
        db.session.commit()

        return jsonify({
            "message": "Order created successfully.",
            "order": new_order.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()  # Rollback in case of any errors
        return jsonify({"error": "Failed to create order.", "details": str(e)}), 500
 """