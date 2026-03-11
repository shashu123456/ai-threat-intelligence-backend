from flask import Blueprint, request, jsonify
from models import User
from database import db
import jwt

auth_bp = Blueprint("auth", __name__)

SECRET = "secret123"

@auth_bp.route("/auth/register", methods=["POST"])
def register():

    data = request.json

    user = User(
        email=data["email"],
        password=data["password"]
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "registered"}

@auth_bp.route("/auth/login", methods=["POST"])
def login():

    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if not user:
        return {"error": "user not found"}, 401

    token = jwt.encode(
        {"email": user.email},
        SECRET,
        algorithm="HS256"
    )

    return {"token": token}