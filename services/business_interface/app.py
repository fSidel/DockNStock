from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, or_
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config import Config
from datetime import *
import requests
import re
import secrets
import logging
import os
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=40)
app.config.from_object(Config)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page"

class Supermarkets(UserMixin):
    def __init__(self, supermarket_id, username):
        self.id = supermarket_id
        self.supermarketname = username

class Products:
    def __init__(self, id: int, name: str, weight: str, photo: str, description: str):
        self.id = id
        self.name = name
        self.weight = weight
        self.photo = photo
        self.description = description

@login_manager.user_loader
def load_user(user_id):
    jsn_data = requests.get(f'http://db_api:5000/supermarkets/{user_id}')
    spr_data_for_login = jsn_data.json()["supermarket"]
    puppet_spr = Supermarkets(
        spr_data_for_login["id"], spr_data_for_login["supermarketname"]
    )
    return puppet_spr 
   #there are no checks!

def verify_password(password):
    if re.match(r'^(?=.*[A-Z])(?=.*\W).{8,}$', password):
        return True
    else:
        return False

def generate_reset_token():
    return secrets.token_urlsafe(32)


#register page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get('username_input')
        password = request.form.get("password_input1")
        password_verify = request.form.get("password_input2")
        password_ok = verify_password(password_verify)

        json_data = {
            'username': username,
            'password': password,
        }
        if password == password_verify and password_ok:
            user = requests.post('http://db_api:5000/supermarkets/register', json=json_data)
            if user.status_code == 201: 
                #user is correctly registered
                user_data = user.json()["supermarket"]
                puppet_superm_id = user_data["id"]
                puppet_superm_dat_id = user_data["supermarketname"]
                spr = Supermarkets(puppet_superm_id, puppet_superm_dat_id)
                login_user(spr)                     
                return redirect(url_for("home"))
            elif user.status_code == 409: 
                return render_template("signup.html", user_alive=True)
            else:
                return "user doesn't have a password or a username"
        else:
            return render_template("signup.html", password_ok=password_ok, password=password, password_verify=password_verify)
    else:
        return render_template("signup.html")
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username_input")
        password_verify = request.form.get("password_input")
        print(username, password_verify, flush=True)
        json_data = {
            'username': username,
            'password': password_verify,
        }
        user = requests.post('http://db_api:5000/supermarkets/login', json=json_data)
        if user.ok:    
            user_data = user.json()["supermarket"]
            spr = Supermarkets(user_data["id"], user_data["supermarketname"])
            login_user(spr)            
            return redirect(url_for("home"))
        else:
            return render_template("login.html", something_failed = True, user_not_found = False)
    elif current_user.is_authenticated:
        print("Already logger in", flush=True)
        return redirect(url_for("main_route"))
    else:
        return render_template("login.html", something_failed = False)

@app.route("/")
def main_route():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        return redirect(url_for("register"))

@app.route('/<something>')
def goto(something):
    return redirect(url_for('main_route'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main_route"))

@app.route('/forget', methods = ["GET", "POST"])
def forgotpasswd():
    if request.method == "POST":
        username = request.form.get('username_input')
        print(username, flush=True)

        print("Retreving User..", flush=True)
        user = requests.post('http://db_api:5000/users/present', 
                             json={"username" : username})

        if not user:
            return render_template("forgot.html", user_alive = False, email_sent = False)

        token = generate_reset_token()
        token += username
        
        msg = Message('Reset Password', sender = Config.MAIL_USERNAME, recipients=[username])
        msg.body = (
            "We received a new password reset request.\n"
            "Click on this link to reset the password: "
            f"{url_for('confirm_forget', token=token, _external=True)}\n"
            "If you did not request this, please ignore this email."
        )
        mail.send(msg)        
        return render_template("forgot.html", user_alive = True, email_sent = True)

    else:
        return render_template("forgot.html")
    
@app.route('/forget/<token>/confirm', methods = ["GET", "POST"])
def confirm_forget(token):
    if request.method == "POST":
        email = token[43:]
        print(email)
        password = request.form.get("password_input1")
        password_verify = request.form.get("password_input2")

        password_ok = verify_password(password_verify)

        print(password, flush=True)
        print(password_verify, flush=True)
        print(password_ok, flush=True)
        
        user = requests.post('http://db_api:5000/users/present', 
                             json={"username" : email})
        if not user:
            return render_template("forgot.html", user_alive = False, password_match = True, password_quality = True, email_sent = False)
        
        if password == password_verify and password_ok:
            print("Updating Password..", flush=True)
            print(password_verify, flush=True)
            user.password = password_verify
            requests.post('http://db_api:5000/users/change_password',
                             json={"username" : email, "password" : password_verify}) 

            return redirect(url_for("login"))
        
        elif not password_ok:
            return render_template("confirm_forgot.html", password_quality = False)
            
        elif password != password_verify:
            return render_template("confirm_forgot.html", password_match = False)
        
    else:
        return render_template("confirm_forgot.html")



@app.route("/home")
@login_required
def home():
    return redirect(url_for('available_products'))


@app.route("/add_products", methods=["GET", "POST"])
@login_required
def add_product():
    
    if request.method == 'POST':
        # 1. Get form data
        name = request.form.get("name")
        weight = request.form.get("weight")
        description = request.form.get("description")
        quantity = int(request.form.get("quantity", 0))
        image_url = request.form.get('imageUrl') 
        

        parameters= {"name" : name, 
                     "weight": weight,
                     "description": description,
                     "photo": image_url
                     }
        

        add_product = requests.post("http://db_api:5000/products", json=parameters)

        if not add_product.ok:
            raise Exception("PRODUCT NOT CREATED!")        
        
        prod_id = add_product.json()
        prod_id = prod_id["product"]
        prod_id = prod_id["id"]
        
        parameters =  {"product_id": prod_id,
                     "supermarket_id": current_user.id,
                     "quantity": quantity
                     }
        
        add_owning = requests.post("http://db_api:5000/owns", json=parameters)
        if not add_owning.ok:
            raise Exception("OWNING NOT CREATED!")        
        return render_template("add_product.html")

    # If GET → render the form
    return render_template("add_product.html")

@app.route('/available_products', methods=["GET"])
@login_required
def available_products():
    response = requests.get(f"http://db_api:5000/owns/{current_user.id}")
    
    if response.ok:
        products = response.json()  
    else:
        products = []  

    return render_template("available_products.html", products=products)

@app.route('/update_quantity', methods=["POST"])
@login_required
def update_quantity():
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    print(f"Received product_id: {product_id}, quantity: {quantity}")

    if not product_id or quantity is None:
        return jsonify({"error": "Product ID and quantity are required"}), 400

    payload = {
        "supermarket_id": current_user.id,
        "product_id": product_id,
        "quantity": quantity
    }
    response = requests.put("http://db_api:5000/owns", json=payload)

    if response.ok:
        return jsonify({"message": "Quantity updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update quantity in the database"}), response.status_code


@app.route('/update_product', methods=["POST"])
@login_required
def update_product():
    """Update all attributes of a product in the database."""
    data = request.json
    product_id = data.get("product_id")
    name = data.get("name")
    weight = data.get("weight")
    photo = data.get("photo")
    description = data.get("description")

    # Validate that all fields are provided
    if not product_id or not name or not weight or not photo or not description:
        return jsonify({"error": "All fields (product_id, name, weight, photo, description) are required"}), 400

    # Update each attribute using the respective API
    errors = []

    # Update name
    response = requests.put(f"http://db_api:5000/products/{product_id}/name", json={"name": name})
    if not response.ok:
        errors.append("Failed to update name")

    # Update weight
    response = requests.put(f"http://db_api:5000/products/{product_id}/weight", json={"weight": weight})
    if not response.ok:
        errors.append("Failed to update weight")

    # Update photo
    response = requests.put(f"http://db_api:5000/products/{product_id}/image", json={"photo": photo})
    if not response.ok:
        errors.append("Failed to update photo")

    # Update description
    response = requests.put(f"http://db_api:5000/products/{product_id}/description", json={"description": description})
    if not response.ok:
        errors.append("Failed to update description")

    # Check for errors
    if errors:
        return jsonify({"error": "Failed to update product", "details": errors}), 500

    return jsonify({"message": "Product updated successfully"}), 200

@app.route('/update_product_form', methods=["POST"])
@login_required
def update_product_form():
    """Retrieve product details and render the modify_product.html form."""
    product_id = request.form.get('product_id')

    print(f"Received product_id: {product_id}")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # Fetch product details from the db_api
    response = requests.get(f"http://db_api:5000/products/{product_id}")
    
    if response.ok:
        product = response.json()  # Parse the product data
    else:
        return jsonify({"error": "Failed to fetch product details"}), response.status_code

    # Render the modify_product.html template with the product data
    return render_template("modify_product.html", product=product)

@app.route("/incoming_orders")
@login_required
def incoming_orders():
    """
    View all orders assigned to the current supermarket, grouped by user.
    """
    supermarket_id = current_user.id
    print(f"Supermarket ID: {supermarket_id}")  # Debugging line

    # Call the API route that groups orders by user
    response = requests.get(f"http://db_api:5000/supermarket_orders/grouped/{supermarket_id}")

    grouped_orders = response.json()  # This will be a dict: {user_id: [orders]}
    print(f"Grouped Orders: {grouped_orders}")  # Debugging lin

    return render_template("incoming_orders.html", grouped_orders=grouped_orders)