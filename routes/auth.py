from flask import Blueprint,request
from flask_jwt_extended import create_access_token
import bcrypt

from database import get_connection

auth_bp = Blueprint("auth",__name__)

@auth_bp.route("/register",methods=["POST"])
def register():

    data=request.get_json()

    email=data["email"]
    password=data["password"]

    hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("INSERT INTO users(email,password) VALUES(%s,%s)",
                   (email,hashed))

    conn.commit()
    conn.close()

    return {"message":"user created"}

@auth_bp.route("/login",methods=["POST"])
def login():

    data=request.get_json()

    email=data["email"]
    password=data["password"]

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT password FROM users WHERE email=%s",(email,))

    row=cursor.fetchone()

    conn.close()

    if row and bcrypt.checkpw(password.encode(),row[0].encode()):

        token=create_access_token(identity=email)

        return {"access_token":token}

    return {"error":"invalid credentials"}