from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from datetime import timedelta
import logging

from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.admin import admin_bp

app = Flask(__name__)
import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password BLOB,
        role TEXT,
        created_at TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        url TEXT,
        prediction TEXT,
        confidence REAL,
        risk_score INTEGER,
        ip TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# CONFIGURATION
# =========================

app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# =========================
# INITIALIZATIONS
# =========================

jwt = JWTManager(app)
CORS(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "20 per hour"]
)

# Logging Setup
logging.basicConfig(level=logging.INFO)

# =========================
# REGISTER BLUEPRINTS
# =========================

app.register_blueprint(auth_bp)
app.register_blueprint(scan_bp)
app.register_blueprint(admin_bp)

# =========================
# ROOT
# =========================

@app.route("/")
def home():
    return jsonify({
        "message": "AI Threat Intelligence Backend Running",
        "endpoints": ["/register", "/login", "/scan", "/history", "/admin/stats"]
    })

if __name__ == "__main__":
    app.run(debug=True)