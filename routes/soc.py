from flask import Blueprint, jsonify
from models import URLScan

soc_bp = Blueprint("soc", __name__)


@soc_bp.route("/timeline")
def timeline():

    scans = URLScan.query.order_by(URLScan.id.desc()).limit(10).all()

    events=[]

    for scan in scans:

        events.append({
            "url":scan.url,
            "prediction":scan.prediction,
            "risk":scan.risk_score
        })

    return {"events":events}