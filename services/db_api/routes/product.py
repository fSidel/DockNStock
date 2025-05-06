from flask import Blueprint, request, jsonify
from flask_login import login_required
from models import Products
from database import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    prod = Products(
        name=data.get('name'),
        weight=data.get('weight'),
        photo=data.get('photo'),
        description=data.get('description')
    )
    db.session.add(prod)
    db.session.commit()
    return jsonify({'message': 'Product created', 'product': prod.to_dict()}), 201

@product_bp.route('/products', methods=['GET'])
def get_products():
    prods = Products.query.all()
    return jsonify([p.to_dict() for p in prods])

@product_bp.route('/products/<int:prod_id>', methods=['GET'])
def get_product(prod_id):
    p = Products.query.get_or_404(prod_id)
    return jsonify(p.to_dict())

@product_bp.route('/products/<int:prod_id>', methods=['PUT'])
def update_product(prod_id):
    p = Products.query.get_or_404(prod_id)
    data = request.get_json()
    for attr in ['name', 'weight', 'photo', 'description']:
        if data.get(attr) is not None:
            setattr(p, attr, data.get(attr))
    db.session.commit()
    return jsonify({'message': 'Product updated', 'product': p.to_dict()})

@product_bp.route('/products/<int:prod_id>', methods=['DELETE'])
def delete_product(prod_id):
    p = Products.query.get_or_404(prod_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})