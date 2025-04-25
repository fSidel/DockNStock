from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash
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
    user = Users(username=username, password=generate_password_hash(password))
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
        login_user(user)
        return jsonify({'message': 'Logged in', 'user': user.to_dict()}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@user_bp.route('/users/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200