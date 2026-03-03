from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
import sqlite3
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

# =========================
# DATABASE CONNECTION
# =========================

def connect_db():
    return sqlite3.connect("database.db")


# =========================
# REGISTER
# =========================

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({"error": "User already exists"}), 400

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Default role = user
    cursor.execute("""
        INSERT INTO users (email, password, role, created_at)
        VALUES (?, ?, ?, ?)
    """, (email, hashed_password, "user", datetime.utcnow()))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "User registered successfully"
    }), 201


# =========================
# LOGIN
# =========================

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, email, password, role FROM users WHERE email=?", (email,))
    user = cursor.fetchone()

    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    user_id, user_email, hashed_password, role = user

    if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
        return jsonify({"error": "Invalid credentials"}), 401

    # 🔥 JWT WITH ROLE CLAIM
    access_token = create_access_token(
        identity=user_email,
        additional_claims={"role": role}
    )

    return jsonify({
        "status": "success",
        "access_token": access_token,
        "role": role
    })