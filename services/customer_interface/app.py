from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, or_
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user
from config import Config
from datetime import *
import requests
import re
import secrets

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=40)
app.config.from_object(Config)
mail = Mail(app)


def verify_password(password):
    if re.match(r'^(?=.*[A-Z])(?=.*\W).{8,}$', password):
        return True
    else:
        return False

def generate_reset_token():
    return secrets.token_urlsafe(32)

#home page

@app.route("/home")
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
    products = requests.get('http://db_api:5000/products/get')
    


    if 'username' in session and 'password' in session and 'id' in session:
        user_id = session['id']
        liked_photos = [city.photo for city in liked_products]  #N.B. liked_products è un json
 
        saved_cities = db.session.query(Cities.photo).join(Saves, Cities.id == Saves.cities_id).filter(Saves.users_id == user_id).all()
        saved_photos = [city.photo for city in saved_cities]
    else:
        liked_photos = []
        saved_photos = []

    # random.shuffle(cities)

    return render_template("index.html", cities=cities, liked=liked_photos, saved=saved_photos, db_comments = list(reversed(truncated_comments)))


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

        user = requests.post('http://db_api:5000/users/register', json=json_data)

        if user.ok:
            return render_template("signup.html", user_alive = True)

        if password == password_verify and password_ok:
            print("HERE")
            user = requests.post('http://db_api:5000/users/login', json=json_data)
            if user.ok:
                #vedere come gestire
                session.permanent = True
                
                session['username'] = username
                user_json = user.json()
                session['id'] = user_json['user']['id']

                #return redirect(url_for("main_route"))
                return redirect(url_for("main"))
            else:
                return "SOMETHING BAD HAPPENED! (tipo username > x caratteri)"
        else:
            return render_template("signup.html", password_ok=password_ok, password=password, password_verify=password_verify)
    elif 'username' in session and 'password' in session:
        return "bo"
        #return redirect(url_for("main_route"))
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
            user_data = user.json()['user']
            session['username'] = username
            session['id'] = user_data['id']
            return redirect(url_for("home"))
        else:
            return render_template("login.html", something_failed = True, user_not_found = False)
        
    elif 'username' in session and 'id' in session:
        print("Already logger in", flush=True)
        return redirect(url_for("main_route"))
    
    else:
        return render_template("login.html", something_failed = False)

@app.route("/")
def main_route():
    return redirect(url_for("login"))

@app.route('/<something>')
def goto(something):
    return redirect(url_for('main_route'))

@app.route("/logout")
def logout():
    logout_user()
    session.clear()

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
