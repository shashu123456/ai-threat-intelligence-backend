from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class ScanLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500))
    result = db.Column(db.String(50))
    risk_score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)