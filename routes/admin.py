from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import get_scan_stats

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/stats", methods=["GET"])
@jwt_required()
def admin_stats():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    stats = get_scan_stats()

    return jsonify({
        "status": "success",
        "data": stats
    })