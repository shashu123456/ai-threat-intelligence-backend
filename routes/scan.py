from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

import pickle

from database import get_connection

scan_bp = Blueprint("scan", __name__)

model = pickle.load(open("phishing_model.pkl", "rb"))


@scan_bp.route("/url", methods=["POST"])
@jwt_required()
def scan_url():

    data = request.get_json()

    url = data["url"]

    features = [len(url), url.count("."), url.count("-"), url.count("@")]

    prediction = model.predict([features])[0]

    confidence = model.predict_proba([features])[0].max()

    result = "phishing" if prediction == 1 else "safe"

    risk_score = int(confidence * 100)

    user = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO scans (user_email,url,prediction,confidence,risk_score,ip) VALUES (%s,%s,%s,%s,%s,%s)",
        (user, url, result, confidence, risk_score, request.remote_addr)
    )

    conn.commit()
    conn.close()

    return {
        "url": url,
        "prediction": result,
        "confidence": confidence,
        "risk_score": risk_score
    }


@scan_bp.route("/history", methods=["GET"])
@jwt_required()
def history():

    user = get_jwt_identity()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT url,prediction,confidence,risk_score,timestamp FROM scans WHERE user_email=%s",
        (user,)
    )

    rows = cursor.fetchall()

    conn.close()

    history = []

    for r in rows:

        history.append({
            "url": r[0],
            "prediction": r[1],
            "confidence": r[2],
            "risk_score": r[3],
            "timestamp": str(r[4])
        })

    return {"history": history}