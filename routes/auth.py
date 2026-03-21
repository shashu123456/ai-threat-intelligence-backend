from flask import Blueprint, request, redirect, render_template, session
from models import User
from extensions import db, bcrypt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            return "Missing fields ❌"

        existing = User.query.filter_by(email=email).first()
        if existing:
            return "User already exists ❌"

        hashed = bcrypt.generate_password_hash(password).decode()

        user = User(email=email, password=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect("/auth/login")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session["user_id"] = user.id
            return redirect("/dashboard")

        return "Invalid credentials ❌"

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/auth/login")