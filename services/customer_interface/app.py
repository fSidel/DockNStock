from flask import Flask, render_template, request
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.datetime.now()
    return render_template('welcome.html', current_time=current_time)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    match request.method:
        case 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            return render_template('welcome.html')
        case 'GET':
            return render_template('signup.html')
