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

@app.route('/addtowants', methods=["POST"])
def addtowants():
    form_sent = request.form

    if current_user.is_authenticated:
        product_id = form_sent.getlist('primarykey')[0]

        data = {
            "user_id": current_user.id,
            "product_id": product_id,
            "quantity": 1
        }

        wants_response = requests.post("http://db_api:5000/wants", json=data)

        if not wants_response.ok:
            print(f"status code of wants: {wants_response.status_code}")
            raise Exception("Could not add to wants, something went wrong :(")

        if wants_response.status_code == 201:
            print("item added to wants (new entry created)")
            status_code = {"code": "201"}
        elif wants_response.status_code == 200:
            print("item already existed, updated correctly in wants")
            status_code = {"code": "200"}
        else:
            print(f"Unexpected status code {wants_response.status_code}")
            status_code = {"code": str(wants_response.status_code)}

    else:
        print("user not logged in!")
        status_code = {"code": "400"}

    return jsonify(status_code)

@app.route('/shopping_cart', methods=["GET"])
@login_required
def shopping_cart():
    """Render the shopping_cart.html template with the user's wanted products."""
    # Fetch wanted products from the Wants API
    response = requests.get(f"http://db_api:5000/wants/{current_user.id}")
    
    if not response.ok:
        print(f"Failed to fetch wanted products: {response.status_code}")
        return render_template("shopping_cart.html", cart_items=[])

    wanted_data = response.json()
    cart_items = []

    # Process the wanted products data
    for item in wanted_data:
        product = Products(
            id=item["product_id"],
            name=item["name"],
            weight=item["weight"],
            photo=item["photo"],
            description=item["description"]
        )
        # Optionally, you can store the quantity from the Wants table if needed:
        product.quantity = item.get("quantity", 1)
        cart_items.append(product)

    return render_template("shopping_cart.html", cart_items=cart_items)


@app.route('/shopping_cart_update', methods=["POST"])
@login_required
def shopping_cart_update():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id or quantity is None:
        return jsonify({"error": "Fields 'product_id' and 'quantity' are required."}), 400

    payload = {
        "user_id": current_user.id,
        "product_id": product_id,
        "quantity": quantity
    }

    try:
        response = requests.put("http://db_api:5000/wants", json=payload)

        if response.status_code != 200:
            return jsonify({"error": "Failed to update quantity in db_api.", "details": response.json()}), response.status_code

        return jsonify(response.json()), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Could not connect to db_api.", "details": str(e)}), 500


@app.route('/place_orders', methods=["POST"])
@login_required
def place_orders():
    """
    Attempt to place orders for all products in the user's shopping cart.
    Shows flash messages with products that were placed or cannot be satisfied.
    Removes successfully ordered products from the wants table.
    """
    print("Placing orders for user:", current_user.id)
    
    # Fetch wanted products from the API
    response = requests.get(f"http://db_api:5000/wants/{current_user.id}")
    if not response.ok:
        flash("Failed to fetch wanted products.", "error")
        return redirect(url_for("shopping_cart"))

    wanted_data = response.json()
    satisfied_products = []
    unsatisfied_products = []
    print("Wanted data:", wanted_data)

    # Attempt to place an order for each product
    for item in wanted_data:
        product_id = item["product_id"]
        product_name = item["name"]
        print(f"Trying to place order for product {product_name} (ID: {product_id})")

        payload = {
            "user_id": current_user.id,
            "product_id": product_id
        }

        order_response = requests.post("http://db_api:5000/orders", json=payload)

        if order_response.ok:
            satisfied_products.append(product_name)

            # Remove the product from wants
            remove_payload = {
                "user_id": current_user.id,
                "product_id": product_id
            }
            remove_response = requests.post("http://db_api:5000/wants/remove", json=remove_payload)
            if not remove_response.ok:
                print(f"Failed to remove {product_name} from wants: {remove_response.text}")

        else:
            unsatisfied_products.append(product_name)
            print(f"Failed to place order for {product_name}: {order_response.text}")

    # Set flash messages for server-rendered page
    if satisfied_products:
        flash(f"These products were successfully ordered: {', '.join(satisfied_products)}", "success")
    if unsatisfied_products:
        flash(f"These products cannot be satisfied due to stock limits: {', '.join(unsatisfied_products)}", "error")

    # Redirect to shopping cart page
    return redirect(url_for("shopping_cart"))



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

@app.route('/remove_from_wants', methods=["POST"])
@login_required
def remove_from_wants():
    """Remove a product from the user's wants list."""
    data = request.json
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    # Prepare payload for wants API
    payload = {
        "user_id": current_user.id,
        "product_id": product_id
    }

    # Call the wants API route
    response = requests.post("http://db_api:5000/wants/remove", json=payload)

    if response.ok:
        return jsonify({"message": "Product removed from wants"}), 200
    else:
        return jsonify({"error": "Failed to remove product from wants"}), response.status_code

