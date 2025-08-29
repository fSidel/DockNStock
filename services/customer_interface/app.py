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
logging.basicConfig(level=logging.DEBUG)

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
    #products=Cities.query.all()

    # db_comments = db.session.query(
    #     Users.username,
    #     Comments.cities_id,
    #     Comments.comment
    # ).join(Comments, Users.id == Comments.users_id).all()

    # truncated_comments = []
    # for com in db_comments:
    #     ind = com[0].index('@')
    #     truncated_username = com[0][:ind]  
    #     truncated_comment = (truncated_username,) + com[1:]  
    #     truncated_comments.append(truncated_comment)

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

    # comments = requests.get(f"http://db_api:5000/user_comment/{current_user.id}")
    # if not comments.ok:
    #     raise Exception("Something went wrong while catching comments in /home")
    # comments = comments.json()
    # for comment in comments:
    #     comment_said = comment["comment"]


   

    return render_template("index.html", products=products_list, liked=liked_photos, saved=saved_photos, db_comments = list(reversed(truncated_comments)))

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
            if user.ok: 
                #user is correctly registered
                user_data = user.json()["user"]
                usr = Users(user_data["id"], user_data["username"])
                login_user(usr)                     
                return redirect(url_for("home"))
            else:   
                #user may be logged in    
                user_log = requests.post('http://db_api:5000/users/login', json=json_data)
                if user_log.ok:
                    userlog_data = user_log.json()["user"]
                    usr2 = Users(userlog_data["id"], user_data["username"])
                    login_user(usr2)                     
                    return redirect(url_for("home"))
                else:
                    return "SO CAZZI AOAOAOAOA"
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
