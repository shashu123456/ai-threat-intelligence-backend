from flask import Flask, render_template, redirect
from extensions import db, bcrypt, socketio
from routes.auth import auth_bp
from routes.scan import scan_bp
from routes.chatbot import chat_bp

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

# INIT EXTENSIONS
db.init_app(app)
bcrypt.init_app(app)
socketio.init_app(app)

# REGISTER ROUTES
app.register_blueprint(auth_bp)
app.register_blueprint(scan_bp)
app.register_blueprint(chat_bp)

@app.route("/")
def home():
    return redirect("/auth/login")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    print("🚀 Running on http://127.0.0.1:5000")
    socketio.run(app, host="127.0.0.1", port=5000)