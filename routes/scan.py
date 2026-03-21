from flask import Blueprint, request, jsonify
from services.ai_engine import predict_url
from services.geo_service import get_geo
from services.threat_feed import check_threat_feeds
from extensions import socketio

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan", methods=["POST"])
def scan():
    url = request.json.get("url")

    socketio.emit("log", "URL received...")
    socketio.emit("log", "Extracting features...")

    pred, prob = predict_url(url)

    socketio.emit("log", "Running ML model...")
    socketio.emit("log", "Checking threat intelligence...")

    threat = check_threat_feeds(url)

    socketio.emit("log", "Fetching domain info...")
    geo = get_geo(url)

    socketio.emit("log", "Calculating risk score...")

    risk = int(prob * 100)

    if threat:
        risk += 40

    risk = min(risk, 100)

    # ✅ EXPLANATION (FIXED — INSIDE FUNCTION)
    explanation = []

    if "login" in url:
        explanation.append("Contains login keyword")

    if len(url) > 50:
        explanation.append("URL length suspicious")

    if "@" in url:
        explanation.append("Contains @ symbol")

    socketio.emit("log", "Finalizing analysis...")
    socketio.emit("log", "--------------------------")

    result = {
        "prediction": "PHISHING" if risk > 60 else "SAFE",
        "risk": risk,
        "geo": geo,
        "explanation": explanation
    }

    socketio.emit("scan_result", result)

    return jsonify(result)