from os import environ
from flask import Flask
from database import db
from models import Users, Products
from routes.user import user_bp
from routes.product import product_bp
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:postgres@db:5432/appdb"

db.init_app(app)  
with app.app_context():
    db.create_all()

app.register_blueprint(user_bp)
app.register_blueprint(product_bp)