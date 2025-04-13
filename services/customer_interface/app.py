from flask import Flask, render_template
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
