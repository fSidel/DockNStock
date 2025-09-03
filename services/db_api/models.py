from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import db

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def get_user(username):
        return db.session.query(Users).filter_by(username=username).first()
    
    @staticmethod
    def change_password(username, new_password):
        user = db.session.query(Users).filter_by(username=username).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
        return None

    def get_likes(self):
        likes = db.session.query(Like).filter_by(users_id=self.id).all()
        return [like.products_like for like in likes]

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {"id": self.id, "username": self.username}

class Supermarkets(UserMixin, db.Model):
    __tablename__ = 'supermarkets'
    id = db.Column(db.Integer, primary_key=True)
    supermarketname = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @staticmethod
    def get_supermarket(supermarketname):
        return db.session.query(Supermarkets).filter_by(supermarketname=supermarketname).first()
    
    @staticmethod
    def change_password(supermarketname, new_password):
        supermarket = db.session.query(Supermarkets).filter_by(supermarketname=supermarketname).first()
        if supermarket:
            supermarket.set_password(new_password)
            db.session.commit()
        return None

    # def get_products of supermarket(self, supid):
    #     products = SELECT TABLETODEFINE.PRODUCTS FROM TABLETODEFINE JOIN SUPERMARKETS ON SUP.supid = TABLETODEFINE.supid
    #     return all products

    def __init__(self, supermarketname=None, password=None):
        self.supermarketname = supermarketname
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<Supermarket {self.supermarketname}>'

    def to_dict(self):
        return {"id": self.id, "supermarketname": self.supermarketname}

class Products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable=False)
    photo = db.Column(db.String(10000), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    def __init__(self, name=None, weight=None, photo=None, description=None):
        self.name = name
        self.weight = weight
        self.photo = photo
        self.description = description

    def __repr__(self):
        return f'<Product {self.name}>'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "weight": self.weight,
            "photo": self.photo,
            "description": self.description,
        }

class Like(db.Model):
    __tablename__ = 'likes'
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key = True)

    users_like = db.relationship("Users", backref=db.backref("users_like", uselist=False))
    products_like = db.relationship("Products", backref=db.backref("products_like", uselist=False))

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    comment = db.Column(db.String(1000), nullable=True)

    users_comments = db.relationship("Users", backref=db.backref("users_comments", uselist=False))
    product_has_comments = db.relationship("Products", backref=db.backref("products_has_comment", uselist=False))

class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    products_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    users_puts_in_cart = db.relationship("Users", backref=db.backref("users_puts_in_cart", uselist=False))
    product_put_in_cart = db.relationship("Products", backref=db.backref("product_put_in_cart", uselist=False))
