from flask import Blueprint, request, jsonify
from models import Supermarkets
from database import db

supermarket_bp = Blueprint('supermarket', __name__)

@supermarket_bp.route('/supermarkets/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if Supermarkets.query.filter_by(supermarketname=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    supermarket = Supermarkets(supermarketname=username, password=password)
    db.session.add(supermarket)
    db.session.commit()
    
    return jsonify({'message': 'User registered', 'supermarket': supermarket.to_dict()}), 201


@supermarket_bp.route('/supermarkets/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    supermarket = Supermarkets.query.filter_by(supermarketname=username).first()
    if supermarket and supermarket.check_password(password): 
        return jsonify({'message': 'Logged in', 'supermarket': supermarket.to_dict()}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

#Gio, I just wrote another route to check the presence of a user so that I don't mess up with the username as the
#key parameter for the query above.
@supermarket_bp.route('/supermarkets/<int:user_id>', methods=['GET'])
def check_user(user_id):
    user = Supermarkets.query.get(user_id)  # get by primary key
    if user:
        return jsonify({"exists": True, "supermarket": user.to_dict()})
    else:
        return jsonify({"exists": False, "message": "User not found"}), 404



@supermarket_bp.route("/supermarkets/change_password", methods=["POST"])
def change_password():
    data = request.get_json()
    username = data.get("username")
    new_password = data.get("password")

    print(f"target account {username}", flush=True)
    print(f"Request to change password to {new_password}", flush=True)
    user = Supermarkets.query.filter_by(supermarketname=username).first()
    if user:
        user.set_password(new_password)
        db.session.commit()
        print("Password changed", flush=True)
        return jsonify({'message': 'Password changed successfully'}), 200
    
    return jsonify({'error': 'User not found'}), 404