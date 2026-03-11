from flask import Blueprint, request, jsonify
from models import URLScan
from database import db
import random

# create blueprint
scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan", methods=["POST"])
def scan():

    data = request.get_json()

    url = data.get("url")

    # demo prediction
    prediction = random.choice(["phishing", "safe"])

    risk_score = random.randint(20, 90)

    # store in database
    scan_record = URLScan(
        url=url,
        prediction=prediction,
        risk_score=risk_score
    )

    db.session.add(scan_record)
    db.session.commit()

    # fake location for map
    location = {
        "lat": 28.61,
        "lon": 77.20,
        "city": "Delhi"
    }

    return jsonify({
        "prediction": prediction,
        "risk_score": risk_score,
        "location": location
    })