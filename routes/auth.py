from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
import bcrypt

from database import get_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO users (email, password, role) VALUES (%s,%s,%s)",
            (email, hashed, "user")
        )

        conn.commit()

    except Exception as e:

        conn.close()
        return {"error": "User already exists"}

    conn.close()

    return {"message": "User registered successfully"}


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data["email"]
    password = data["password"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password FROM users WHERE email=%s",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return {"error": "Invalid credentials"}

    if not bcrypt.checkpw(password.encode(), user[0].tobytes()):
        return {"error": "Invalid credentials"}

    token = create_access_token(identity=email)

    return {"access_token": token}