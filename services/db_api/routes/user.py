from flask import Blueprint, request, jsonify
from models import Users
from database import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if Users.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 409
    
    user = Users(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered', 'user': user.to_dict()}), 201


@user_bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = Users.query.filter_by(username=username).first()
    
    if user and user.check_password(password): 
        return jsonify({'message': 'Logged in', 'user': user.to_dict()}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401


@user_bp.route("/users/present", methods=["POST"])
def present():
    data = request.get_json()
    username = data.get("username")

    print(username, flush=True)
    print("Retreving User..", flush=True)

    user = Users.get_user(username)
    if user:
        print(user, flush=True)
        print("User found", flush=True)
        print(user.to_dict(), flush=True)

        return jsonify({'message': 'Logged in', 'user': user.to_dict()}), 200
    return jsonify({'error': 'User not found'}), 401
    

@user_bp.route("/users/change_password", methods=["POST"])
def change_password():
    data = request.get_json()
    username = data.get("username")
    new_password = data.get("new_password")

    user = Users.query.filter_by(username=username).first()
    if user:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    
    return jsonify({'error': 'User not found'}), 404