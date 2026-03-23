import os
from flask import Flask, render_template
from flask_login import login_required
from extensions import db, login_manager, socketio, limiter
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)

    # ── Configuration ──────────────────────────────────────────────────────────
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(32).hex())
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///threat_intel.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}

    # API Keys (optional — gracefully degraded if absent)
    app.config["GOOGLE_SAFE_BROWSING_KEY"] = os.getenv("GOOGLE_SAFE_BROWSING_KEY", "")
    app.config["ABUSEIPDB_KEY"] = os.getenv("ABUSEIPDB_KEY", "")
    app.config["VIRUSTOTAL_KEY"] = os.getenv("VIRUSTOTAL_KEY", "")

    # ── Extensions ─────────────────────────────────────────────────────────────
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode="threading",
        logger=False,
        engineio_logger=False,
    )
    limiter.init_app(app)

    # ── User loader ────────────────────────────────────────────────────────────
    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ── Blueprints ─────────────────────────────────────────────────────────────
    from routes.auth import auth_bp
    from routes.scan import scan_bp
    from routes.chatbot import chatbot_bp
    from routes.logs import logs_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(scan_bp, url_prefix="/api")
    app.register_blueprint(chatbot_bp, url_prefix="/api")
    app.register_blueprint(logs_bp, url_prefix="/api")

    # ── Core routes ────────────────────────────────────────────────────────────
    @app.route("/")
    @login_required
    def index():
        return render_template("dashboard.html")

    @app.route("/health")
    def health():
        return {"status": "ok", "service": "CyberShield CTI Platform"}, 200

    # ── DB Init ────────────────────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_demo_logs()

    return app


def _seed_demo_logs():
    """Seed a few demo threat logs so the UI isn't empty on first run."""
    from models import ThreatLog

    if ThreatLog.query.count() == 0:
        seeds = [
            ThreatLog(
                event_type="PORT_SCAN",
                severity="medium",
                message="Port scan detected from 185.220.101.47",
                source_ip="185.220.101.47",
            ),
            ThreatLog(
                event_type="PHISHING_ATTEMPT",
                severity="high",
                message="Phishing URL flagged: secure-paypa1.com",
                source_ip="103.21.244.0",
                target_url="[secure-paypa1.com](http://secure-paypa1.com/login)",
            ),
            ThreatLog(
                event_type="BRUTE_FORCE",
                severity="critical",
                message="SSH brute-force from 45.33.32.156 (422 attempts)",
                source_ip="45.33.32.156",
            ),
        ]
        from extensions import db as _db

        _db.session.bulk_save_objects(seeds)
        _db.session.commit()


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, use_reloader=False)
