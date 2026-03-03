from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from routes.auth import auth_bp
from routes.scan import scan_bp

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(scan_bp)

@app.route("/")
def home():
    return jsonify({
        "message": "AI Threat Intelligence Backend Running",
        "endpoints": ["/register", "/login", "/scan", "/history"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)