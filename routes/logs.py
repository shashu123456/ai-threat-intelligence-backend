from flask import Blueprint, jsonify, request
from models import ThreatLog

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("/logs", methods=["GET"])
def get_logs():
    limit = min(int(request.args.get("limit", 100)), 500)
    severity = request.args.get("severity")

    query = ThreatLog.query.order_by(ThreatLog.created_at.desc())
    if severity:
        query = query.filter_by(severity=severity)

    logs = query.limit(limit).all()
    return jsonify([l.to_dict() for l in logs]), 200
