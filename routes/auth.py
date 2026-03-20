from flask import Blueprint, request, jsonify
from models import User
from extensions import db, bcrypt
from flask_jwt_extended import create_access_token
import re

auth_bp = Blueprint("auth", __name__)

def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[0-9]", password) and
        re.search(r"[!@#$%^&*]", password)
    )

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data['email']
    password = data['password']

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"msg": "Invalid email"}), 400

    if not is_valid_password(password):
        return jsonify({"msg": "Weak password"}), 400

    hashed = bcrypt.generate_password_hash(password).decode()

    user = User(email=email, password=hashed)
    db.session.add(user)
    db.session.commit()

    return jsonify({"msg": "Registered successfully"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify(access_token=token)

    return jsonify({"msg": "Invalid credentials"}), 401