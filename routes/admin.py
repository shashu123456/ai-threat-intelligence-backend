from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from database import get_connection

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/stats")
@jwt_required()
def stats():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({"error": "Admin only"}), 403

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total = cursor.fetchone()[0]

    conn.close()

    return jsonify({"total_scans": total})