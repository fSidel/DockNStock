from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_login import LoginManager, UserMixin, login_user, logout_user   

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
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

db.create_all()
