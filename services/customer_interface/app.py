from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def time():
    current_time = datetime.datetime.now()
    return render_template('welcome.html', current_time=current_time)
