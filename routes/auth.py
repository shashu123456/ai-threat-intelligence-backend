from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt
from database import get_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (email, password, role)
    VALUES (%s, %s, %s)
    """, (email, hashed, "user"))

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT password, role FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    hashed, role = user

    if not bcrypt.checkpw(password.encode(), hashed.tobytes()):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=email, additional_claims={"role": role})

    return jsonify({"access_token": token})