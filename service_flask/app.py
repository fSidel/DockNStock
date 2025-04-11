import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    db_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    now = cur.fetchone()
    cur.close()
    conn.close()
    return f"Database time is: {now[0]}"
