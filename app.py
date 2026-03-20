from flask import Flask
from extensions import db, bcrypt, jwt
from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.analytics import analytics_bp
from routes.chatbot import chatbot_bp

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'supersecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(scan_bp, url_prefix="/scan")
    app.register_blueprint(analytics_bp, url_prefix="/analytics")
    app.register_blueprint(chatbot_bp, url_prefix="/chatbot")

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)