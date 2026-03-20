from flask import Flask, jsonify
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
     commit_sha = os.getenv("COMMIT_SHA", "unknown")
     return jsonify({
          "message": "Hello from Flask API",
          "commit": commit_sha
     })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
