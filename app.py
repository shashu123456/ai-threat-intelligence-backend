from flask import Flask, render_template
from database import db

from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.analytics import analytics_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)

app.register_blueprint(auth_bp)
app.register_blueprint(scan_bp)
app.register_blueprint(analytics_bp)

@app.route("/")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)