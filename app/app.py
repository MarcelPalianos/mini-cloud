from flask import Flask
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "mydb"),
        user=os.getenv("DB_USER", "myuser"),
        password=os.getenv("DB_PASSWORD", "example")
    )
@app.route("/")
def home():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 'Mini Cloud v4 - deploy from Docker Hub'")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return result
    except Exception as e:
        return f"Database connection failed: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)