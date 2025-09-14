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