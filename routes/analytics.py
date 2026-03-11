from flask import Blueprint, jsonify
from models import URLScan

# create blueprint
analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/analytics/stats")
def stats():

    total = URLScan.query.count()

    phishing = URLScan.query.filter_by(
        prediction="phishing"
    ).count()

    safe = URLScan.query.filter_by(
        prediction="safe"
    ).count()

    return jsonify({
        "total_scans": total,
        "phishing": phishing,
        "safe": safe
    })