from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from flasgger import Swagger

from config import Config
from models import create_tables

from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.admin import admin_bp


app = Flask(__name__)

app.config.from_object(Config)

CORS(app)

jwt = JWTManager(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"]
)

swagger = Swagger(app)

create_tables()

app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(scan_bp, url_prefix="/scan")
app.register_blueprint(admin_bp, url_prefix="/admin")


@app.route("/")
def home():
    return {
        "status": "running",
        "project": "AI Threat Intelligence Platform",
        "version": "1.0"
    }


if __name__ == "__main__":
    app.run(debug=True)