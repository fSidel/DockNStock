from flask import Flask
import datetime
app = Flask(__name__)

@app.route('/')
def time():
    return f"Current time is {datetime.datetime.now()}"

app.run()