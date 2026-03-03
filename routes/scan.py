from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.ml_service import analyze_url
from models import save_scan_history
from flask_limiter import Limiter
import logging
from datetime import datetime

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan", methods=["POST"])
@jwt_required()
def scan():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL required"}), 400

    user = get_jwt_identity()
    ip_address = request.remote_addr

    prediction, confidence, risk_score = analyze_url(url)

    # Save to database
    save_scan_history(user, url, prediction, confidence, risk_score, ip_address)

    logging.info(f"User {user} scanned {url} from IP {ip_address}")

    return jsonify({
        "status": "success",
        "data": {
            "url": url,
            "prediction": prediction,
            "confidence_percentage": confidence,
            "risk_score": risk_score,
            "scanned_by": user,
            "ip_address": ip_address,
            "timestamp": datetime.utcnow().isoformat()
        }
    })