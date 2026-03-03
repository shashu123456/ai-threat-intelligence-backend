from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlite3
import datetime
from config import Config
from services.ml_service import analyze_url

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan", methods=["POST"])
@jwt_required()
def scan():
    current_user = get_jwt_identity()
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "URL required"}), 400

    url = data["url"]

    prediction, confidence, risk_score = analyze_url(url)

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            url TEXT,
            prediction TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO scans (username, url, prediction, confidence, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (current_user, url, prediction, confidence, str(datetime.datetime.now())))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "data": {
            "url": url,
            "prediction": prediction,
            "confidence_percentage": confidence,
            "risk_score": risk_score,
            "scanned_by": current_user
        }
    }), 200


@scan_bp.route("/history", methods=["GET"])
@jwt_required()
def history():
    current_user = get_jwt_identity()

    conn = sqlite3.connect(Config.DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT url, prediction, confidence, timestamp FROM scans WHERE username = ?",
        (current_user,)
    )
    results = cursor.fetchall()
    conn.close()

    return jsonify(results), 200