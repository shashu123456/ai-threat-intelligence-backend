from flask import Blueprint, jsonify
from models import ScanLog

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/")
def stats():
    total = ScanLog.query.count()
    phishing = ScanLog.query.filter_by(result="PHISHING").count()
    safe = ScanLog.query.filter_by(result="SAFE").count()

    return jsonify({
        "total": total,
        "phishing": phishing,
        "safe": safe
    })