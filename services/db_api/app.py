from os import environ
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@db:5432/appdb"
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)    
    username = db.Column(db.String(30), nullable = False, unique = True)    
    password = db.Column(db.String(250), nullable = False)

    def __init__(self, username = None,password = None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username}, password {self.password}>'
    

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(20), nullable = False)
    weight = db.Column(db.String(20), nullable = False)
    photo = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(250), nullable = False)

    def __init__(self, name=None, weight=None, photo=None, description=None):
        self.name = name
        self.weight = weight
        self.photo = photo
        self.description = description

    def __repr__(self):
        return f'<Product {self.name}, weight: {self.weight}, photo: {self.photo}, description: {self.description}>'


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Auth Routes
@app.route('/users/register', methods=['POST'])
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

@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': 'Logged in', 'user': user.to_dict()}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/users/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200

# User CRUD
def user_to_response(user):
    return jsonify(user.to_dict())

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    users = Users.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = Users.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    user = Users.query.get_or_404(user_id)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username:
        user.username = username
    if password:
        user.password = generate_password_hash(password)
    db.session.commit()
    return jsonify({'message': 'User updated', 'user': user.to_dict()})

@app.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})



######## Product CRUD



@app.route('/products', methods=['POST'])
@login_required
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

@app.route('/products', methods=['GET'])
def get_products():
    prods = Products.query.all()
    return jsonify([p.to_dict() for p in prods])

@app.route('/products/<int:prod_id>', methods=['GET'])
def get_product(prod_id):
    p = Products.query.get_or_404(prod_id)
    return jsonify(p.to_dict())

@app.route('/products/<int:prod_id>', methods=['PUT'])
@login_required
def update_product(prod_id):
    p = Products.query.get_or_404(prod_id)
    data = request.get_json()
    for attr in ['name', 'weight', 'photo', 'description']:
        if data.get(attr) is not None:
            setattr(p, attr, data.get(attr))
    db.session.commit()
    return jsonify({'message': 'Product updated', 'product': p.to_dict()})

@app.route('/products/<int:prod_id>', methods=['DELETE'])
@login_required
def delete_product(prod_id):
    p = Products.query.get_or_404(prod_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})
