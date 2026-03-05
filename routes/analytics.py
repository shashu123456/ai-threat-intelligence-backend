from flask import Blueprint
from database import get_connection

analytics_bp = Blueprint("analytics",__name__)

@analytics_bp.route("/stats")

def stats():

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE prediction='phishing'")
    phishing=cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE prediction='safe'")
    safe=cursor.fetchone()[0]

    conn.close()

    return {

        "total_scans":total,
        "phishing_detected":phishing,
        "safe_urls":safe

    }