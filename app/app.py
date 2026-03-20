from flask import Flask, jsonify, request
from prometheus_client import Counter, generate_latest
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

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            text TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['endpoint'])

@app.route("/health")
def health():
	return "OK", 200

@app.route("/")
def home():
    commit_sha = os.getenv("COMMIT_SHA", "unknown")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 'Mini Cloud v9- Final deploy script + frontend connection + rebuild web and backend'")
        result = cur.fetchone()[0]
        cur.close()
        conn.close()
        return f"{result} - commit {commit_sha}"
    except Exception as e:
        return f"Database connection failed - commit {commit_sha} - error: {e}", 500

@app.route("/api/message")
def api_message():
    REQUEST_COUNT.labels(endpoint='/api/message').inc()
    ommit_sha = os.getenv("COMMIT_SHA", "unknown")
    return jsonify({
        "message": "Hello from Flask API",
        "commit": commit_sha
     })

@app.route("/api/add", methods=["POST"])
def add_message():
    data = request.get_json()
    message = data.get("message", "")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (text) VALUES (%s)", (message,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "ok"})

@app.route("/api/messages")
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([
        {"id": row[0], "text": row[1]}
        for row in rows
    ])
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain'}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
