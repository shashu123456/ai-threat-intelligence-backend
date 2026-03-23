from flask import Blueprint, request, jsonify
from services.ai_engine import predict_url
from services.geo_service import get_geo
from services.threat_intel import check_google_safe, check_abuse_ip
from extensions import socketio

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan", methods=["POST"])
def scan():
    try:
        data = request.get_json()
        url = data.get("url")

        socketio.emit("log", "URL received...")
        socketio.emit("log", "Extracting features...")

        pred, prob = predict_url(url)

        socketio.emit("log", "Running ML model...")

        geo = get_geo(url)
        ip = geo.get("ip")

        socketio.emit("log", f"Resolved IP: {ip}")

        google_threat = check_google_safe(url)
        abuse_threat = check_abuse_ip(ip)

        socketio.emit("log", "Calculating risk score...")

        risk = int(prob * 100)

        if google_threat:
            risk += 30

        if abuse_threat:
            risk += 30

        risk = min(risk, 100)

        explanation = []

        if url:
            if "login" in url:
                explanation.append("Contains login keyword")
            if len(url) > 50:
                explanation.append("Suspicious long URL")
            if "@" in url:
                explanation.append("Contains @ symbol")

        if google_threat:
            explanation.append("Flagged by Google Safe Browsing")

        if abuse_threat:
            explanation.append("Malicious IP (AbuseIPDB)")

        result = {
            "prediction": "PHISHING" if risk > 60 else "SAFE",
            "risk": risk,
            "geo": geo,
            "explanation": explanation,
            "active": True if risk > 60 else False
        }

        socketio.emit("scan_result", result)

        return jsonify(result)

    except Exception as e:
        print("SCAN ERROR:", e)
        return jsonify({"error": str(e)}), 500