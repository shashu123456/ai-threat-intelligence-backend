from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flasgger import Swagger

from config import Config
from utils.logger import setup_logger
from models import create_tables

from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.config.from_object(Config)

JWTManager(app)
CORS(app)
Swagger(app)

limiter = Limiter(get_remote_address, app=app, default_limits=["100 per day"])

setup_logger()
create_tables()

app.register_blueprint(auth_bp)
app.register_blueprint(scan_bp)
app.register_blueprint(admin_bp)

@app.route("/")
def home():
    return jsonify({
        "message": "AI Threat Intelligence Platform Running",
        "docs": "/apidocs"
    })

if __name__ == "__main__":
    app.run(debug=True)