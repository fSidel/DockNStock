from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc, or_
from flask_mail import Mail, Message
from flask_login import LoginManager, UserMixin, login_user, logout_user
from datetime import *
import random
import os

app = Flask(__name__)

#register page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get('username_input')
        password = request.form.get("password_input1")
        password_verify = request.form.get("password_input2")

        #cambiare
        password_ok = verify_password(password_verify)

        #vedere come fare la query
        user = Users.query.filter_by(username = username).first()

        if user:
            return render_template("signup.html", user_alive = True)

        if password == password_verify and password_ok:
            user = Users(username, password)
            db.session.add(user)
            db.session.commit()

            #vedere come gestire
            session.permanent = True
            
            session['username'] = username
            session['password'] = password
            session['id'] = user.id

            return redirect(url_for("main_route"))
        else:
            return render_template("signup.html", password_ok=password_ok, password=password, password_verify=password_verify)
    elif 'username' in session and 'password' in session:
        return redirect(url_for("main_route"))
    else:
        return render_template("signup.html")
    
