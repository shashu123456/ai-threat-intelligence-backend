from extensions import db
from flask_login import UserMixin
from datetime import datetime
import json


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scans = db.relationship("ScanResult", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class ScanResult(db.Model):
    __tablename__ = "scan_results"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    url = db.Column(db.String(2048), nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    prediction = db.Column(db.String(20), nullable=False)  # "phishing" | "safe"
    confidence = db.Column(db.Float, nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    features_json = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(64), nullable=True)
    geo_data_json = db.Column(db.Text, nullable=True)
    threat_data_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "risk_score": self.risk_score,
            "prediction": self.prediction,
            "confidence": self.confidence,
            "explanation": self.explanation,
            "features": json.loads(self.features_json) if self.features_json else {},
            "ip_address": self.ip_address,
            "geo_data": json.loads(self.geo_data_json) if self.geo_data_json else {},
            "threat_data": json.loads(self.threat_data_json) if self.threat_data_json else {},
            "created_at": self.created_at.isoformat(),
        }


class ThreatLog(db.Model):
    __tablename__ = "threat_logs"

    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(64), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # low | medium | high | critical
    message = db.Column(db.Text, nullable=False)
    source_ip = db.Column(db.String(64), nullable=True)
    target_url = db.Column(db.String(2048), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "event_type": self.event_type,
            "severity": self.severity,
            "message": self.message,
            "source_ip": self.source_ip,
            "target_url": self.target_url,
            "created_at": self.created_at.isoformat(),
        }
