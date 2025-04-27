import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return f"Hey! Listen!"

