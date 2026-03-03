from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ml_service import analyze_url
from models import save_scan
from config import Config

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan", methods=["POST"])
@jwt_required()
def scan():
    api_key = request.headers.get("X-API-KEY")

    if api_key != Config.API_KEY:
        return jsonify({"error": "Invalid API Key"}), 403

    data = request.get_json()
    url = data.get("url")

    user = get_jwt_identity()
    ip = request.remote_addr

    prediction, confidence, risk_score = analyze_url(url)

    save_scan(user, url, prediction, confidence, risk_score, ip)

    return jsonify({
        "url": url,
        "prediction": prediction,
        "confidence": confidence,
        "risk_score": risk_score
    })