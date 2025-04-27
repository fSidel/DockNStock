from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, or_
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user
from datetime import *
import random
import os
import requests
import re

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=40)
app.config["SECRET_KEY"] = "STOCKNDOCK :)"


def verify_password(password):
    if re.match(r'^(?=.*[A-Z])(?=.*\W).{8,}$', password):
        return True
    else:
        return False
    

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

        user = requests.post('http://db_api:5000/users/login', json=json_data)

        if user.ok:
            return render_template("signup.html", user_alive = True)

        if password == password_verify and password_ok:
            print("HERE")
            user = requests.post('http://db_api:5000/users/register', json=json_data)
            if user.ok:
                #vedere come gestire
                session.permanent = True
                
                session['username'] = username
                user_json = user.json()
                session['id'] = user_json['user']['id']

                #return redirect(url_for("main_route"))
                return "ok till here"
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

        json_data = {
            'username': username,
            'password': password_verify,
        }

        user = requests.post('http://db_api:5000/users/login', json=json_data)
        user_json = user.json()
        password = user_json["debug"]["password_provided"]
        if user.ok and password == password_verify:
            #login_user(user)           
            session['username'] = username
            session['id'] = user_json['user']['id']

            return "qui il redirect al main route"
        
        elif not user:
            return render_template("login.html", something_failed = True, user_not_found = True)
        
        else:
            return render_template("login.html", something_failed = True, user_not_found = False)
        
    elif 'username' in session and 'id' in session:
        return "qui il redirect al main route"
    
    else:
        return render_template("login.html", something_failed = False)

    
app.run(debug=True, host="0.0.0.0")