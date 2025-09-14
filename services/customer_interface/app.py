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
import random
import sys
logging.basicConfig(level=logging.DEBUG,stream=sys.stdout)

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=40)
app.config.from_object(Config)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page"

#I didn't know how to import it :(
class Users(UserMixin):
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username

class Products:
    def __init__(self, id: int, name: str, weight: str, photo: str, description: str):
        self.id = id
        self.name = name
        self.weight = weight
        self.photo = photo
        self.description = description

class Comments:
    def __init__(self, comments_id: int, users_username: str, product_id: int, comment: str):
        self.comment_id = comments_id
        self.username = users_username
        self.product_id = product_id
        self.comment = comment

    def __str__(self):
        return f"Comment(id={self.comment_id}, user={self.username}, product_id={self.product_id}, comment={self.comment})"

# User loader function
@login_manager.user_loader
def load_user(user_id):
    jsn_data = requests.get(f'http://db_api:5000/users/{user_id}')
    usr_data_for_login = jsn_data.json()["user"]
    puppet_usr = Users(
        usr_data_for_login["id"], usr_data_for_login["username"]
    )
    return puppet_usr   #there are no checks!


def verify_password(password):
    if re.match(r'^(?=.*[A-Z])(?=.*\W).{8,}$', password):
        return True
    else:
        return False

def generate_reset_token():
    return secrets.token_urlsafe(32)

#home page
@app.route("/home")
@login_required
def home():

    liked_photos = []
    saved_photos = []   #da lasciare ? BO!
    truncated_comments = [] #da rimuovere

    products_data = requests.get(f'http://db_api:5000/products').json() #aggiungere controlli
    products_list = []
    for pro in products_data:
        product = Products(pro["id"], pro["name"], pro["weight"], pro["photo"], pro["description"])
        products_list.append(product)

    liked_data = requests.get(f"http://db_api:5000/products/like/{current_user.id}").json()  #aggiungere controlli
    liked_list = []
    for like in liked_data:
        liked_product = Products(like["id"], like["name"], like["weight"], like["photo"], like["description"])
        liked_list.append(liked_product)
    
    random.shuffle(products_list)

    comments_response = requests.get(f"http://db_api:5000/get_comments").json()
    print("Comments response from backend:", comments_response)

    comments_list = []
    print("Processing comments...")
    for comment in comments_response:
        print("Processing comment:", comment)
        # Extract the required fields
        comment_id = comment["comment_id"]
        product_id = comment["product"]["id"]
        user_username = comment["user"]["username"]
        comment_text = comment["comment"]

        # Create a Comments object with the extracted fields
        comments_on_product = Comments(comment_id, user_username, product_id, comment_text)
        print("Created Comments object:", comments_on_product.comment_id, comments_on_product.username, comments_on_product.product_id, comments_on_product.comment)

        comments_list.append(comments_on_product)

    for comment in comments_list:
        print("Final comment in list:", comment)

    # comments = requests.get(f"http://db_api:5000/user_comment/{current_user.id}")
    # if not comments.ok:
    #     raise Exception("Something went wrong while catching comments in /home")
    # comments = comments.json()
    # for comment in comments:
    #     comment_said = comment["comment"]

    return render_template("index.html", products=products_list, liked=liked_photos, saved=saved_photos, db_comments = comments_list)

@app.route('/leavealike', methods = ["POST"])
def leave_like():
    form_sent = request.form
    #if user is logged in
    if current_user.is_authenticated:
        product_id = form_sent.getlist('primarykey')[0]
        like_json = requests.post(f"http://db_api:5000/like/{current_user.id}/{product_id}")

        if not like_json.ok:
            print(f"status code of like: {like_json.status_code}")
            raise Exception('could not put like, donno what happened :(')
        
        if like_json.status_code == 201:
            print("removing like")
            status_code = {"code" : "201"}
        elif like_json.status_code == 200:
            print("like inserted correctely in database")
            status_code = {'code' : '200'}
        else:
            print(f"obtain status code {like_json.status_code} bo che è ?!")
    else:
        print('user not logged in!')
        status_code = {'code' : '400'}
    return jsonify(status_code)

@app.route('/addtocart', methods = ["POST"])
def addtocart():
    form_sent = request.form
    #if user is logged in
    if current_user.is_authenticated:
        product_id = form_sent.getlist('primarykey')[0]
        data = {
            "user_id":current_user.id,
            "product_id":product_id
        }
        cart_json = requests.post(f"http://db_api:5000/cart", json=data)
        if not cart_json.ok:
            print(f"status code of cart: {cart_json.status_code}")
            raise Exception('could not put into cart, donno what happened :(')
        
        if cart_json.status_code == 201:
            print("removing item from cart")
            status_code = {"code" : "201"}
        elif cart_json.status_code == 200:
            print("item in cart inserted correctely in database")
            status_code = {'code' : '200'}
        else:
            print(f"obtain status code {cart_json.status_code} bo che è ?!")
    else:
        print('user not logged in!')
        status_code = {'code' : '400'}
    return jsonify(status_code)

@app.route('/shopping_cart', methods = ["GET"])
@login_required
def shopping_cart():
    """Render the shopping_cart.html template with the user's cart items."""
    # Fetch cart items from the cart service
    response = requests.get(f"http://db_api:5000/cart/{current_user.id}")
    
    if not response.ok:
        print(f"Failed to fetch cart items: {response.status_code}")
        return render_template("shopping_cart.html", cart_items=[])

    cart_data = response.json()
    cart_items = []

    # Process the cart data
    for item in cart_data:
        product = Products(
            id=item["product_id"],
            name=item["name"],
            weight=item["weight"],
            photo=item["photo"],
            description=item["description"]
        )
        cart_items.append(product)

    return render_template("shopping_cart.html", cart_items=cart_items)

@app.route('/postcomments', methods = ["POST"])
def post_comments():

    msg_sent = request.form.get('comments')
    product_id = request.form.get('product_key') #cambiare la city key!

    data = {
        "user_id":current_user.id,
        "product_id":product_id,
        "comment":msg_sent
    }

    send_comment = requests.post("http://db_api:5000/comment", json=data)
    if not send_comment.ok:
        print(send_comment.status_code)
        raise Exception("Something went wrong")
    send_comment = send_comment.json()
    return jsonify(
        send_comment["user"]["username"]
    )


@app.route('/likes', methods = ["GET"])
def likes():
    """Render the favorite.html template with the user's likes."""
    likes_data = requests.get(f"http://db_api:5000/users/{current_user.id}/likes").json()
    liked_products = []
    for like in likes_data["likes"]:
        product = Products(like["id"], like["name"], like["weight"], like["photo"], like["description"])
        liked_products.append(product)
    
    return render_template("favorite.html", liked_products=liked_products)

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
            user = requests.post('http://db_api:5000/users/register', json=json_data)
            if user.status_code == 201: 
                #user is correctly registered
                user_data = user.json()["user"]
                puppet_usr_id = user_data["id"]
                puppet_dat_id = user_data["username"]
                usr = Users(puppet_usr_id, puppet_dat_id)
                login_user(usr)                     
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
        user = requests.post('http://db_api:5000/users/login', json=json_data)
        if user.ok:    
            user_data = user.json()["user"]
            usr = Users(user_data["id"], user_data["username"])
            login_user(usr)            
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

@app.route('/remove_from_cart', methods=["POST"])
@login_required
def remove_from_cart():
    """Remove a product from the user's cart."""
    data = request.json
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # Prepare the request payload
    payload = {
        "user_id": current_user.id,
        "product_id": product_id
    }

    # Call the API in cart.py to remove the product
    response = requests.post("http://db_api:5000/cart/remove", json=payload)

    if response.ok:
        return jsonify({"message": "Product removed from cart"}), 200
    else:
        return jsonify({"error": "Failed to remove product from cart"}), response.status_code

@app.route('/place_orders', methods=["POST"])
@login_required
def place_orders():
    # """Send order data to order service and clear items from cart if successful."""
    # data = request.json  # Get the JSON data from the request
    # print("Received order data:", data)  # Debug log

    # if not data or "cart_items" not in data:
    #     return jsonify({"error": "Order data must include cart_items"}), 400

    # try:
    #     # Send order to external order service
    #     response = requests.post(
    #         "http://localhost:5001/receive_orders",
    #         json={
    #             "user_id": current_user.id,
    #             "cart_items": data["cart_items"]
    #         },
    #         timeout=5
    #     )
    # except requests.RequestException as e:
    #     print("Error contacting order service:", e)
    #     return jsonify({"error": "Could not reach order service"}), 502

    # if response.ok:
    #     # Order accepted → remove items from cart
    #     for item in data["cart_items"]:
    #         product_id = item.get("product_id")
    #         if not product_id:
    #             continue

    #         payload = {
    #             "user_id": current_user.id,
    #             "product_id": product_id
    #         }
    #         remove_response = requests.post(
    #             "http://db_api:5000/cart/remove",
    #             json=payload
    #         )
    #         if not remove_response.ok:
    #             print(f"Failed to remove product {product_id} from cart")

    #     return jsonify({"message": "Order placed and cart updated"}), 200
    # else:
    #     return jsonify({"error": "Order service rejected order"}), response.status_code
    data = request.json
    print("Received order:", data)


    #1) trace supermarket having these products
    # SELCT SUPERMARKETS JOIN HAS WHERE SUPERMARKET.ID = PRODUCTS_ID *.first()*

    

    #2) create a order object (supermarket, user)

    #3) delete products.id from saved_in_cart where products.id = data.products_id

    #somehow the supermarket must save which products the user ordered

    # Here you would insert into DB, clear cart, etc.
    return jsonify({"status": "success", "message": "Order placed successfully"}),200
