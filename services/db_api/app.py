from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_login import LoginManager, UserMixin, login_user, logout_user   

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables
    app.run(host='0.0.0.0', port=5000, debug=True)
