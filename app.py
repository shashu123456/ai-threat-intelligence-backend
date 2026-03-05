from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Config
from models import create_tables

from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.analytics import analytics_bp
from routes.soc import soc_bp
from flask import render_template

app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

jwt = JWTManager(app)

limiter = Limiter(get_remote_address, app=app)

create_tables()

app.register_blueprint(auth_bp,url_prefix="/auth")
app.register_blueprint(scan_bp,url_prefix="/scan")
app.register_blueprint(analytics_bp,url_prefix="/analytics")
app.register_blueprint(soc_bp,url_prefix="/soc")


@app.route("/")

def home():

    return {"message":"AI Threat Intelligence API running"}
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

@app.route("/scanner")
def scanner_page():
    return render_template("index.html")


if __name__ == "__main__":

    app.run()