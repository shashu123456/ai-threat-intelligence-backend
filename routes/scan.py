from flask import Blueprint, request, jsonify
from services.ai_engine import predict_url
from services.threat_feed import threat_score
from services.domain_intelligence import analyze_domain
from models import ScanLog
from extensions import db

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/", methods=["POST"])
def scan():
    url = request.json['url']

    pred, ml_score = predict_url(url)
    threat = threat_score(url)
    domain = analyze_domain(url)

    final_score = min(100, ml_score + threat)

    result = "PHISHING" if final_score > 60 else "SAFE"

    log = ScanLog(url=url, result=result, risk_score=final_score)
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "result": result,
        "risk_score": final_score,
        "domain": domain
    })