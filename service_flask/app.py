import os
import psycopg2
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        return "No database URL provided", 500

    # Debugging: Print environment variables
    print(f"DATABASE_URL: {db_url}")
    print(f"POSTGRES_USER: {os.environ.get('POSTGRES_USER')}")
    print(f"POSTGRES_PASSWORD: {os.environ.get('POSTGRES_PASSWORD')}")

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    now = cur.fetchone()
    cur.close()
    conn.close()
    return f"Database time is: {now[0]}"

