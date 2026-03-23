from flask import Blueprint, request, jsonify

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower()

    if "phishing" in msg:
        return jsonify({"reply": "Phishing attacks mimic trusted websites to steal user credentials."})

    if "url" in msg:
        return jsonify({"reply": "Enter a URL in scanner. System will analyze risk using ML + threat APIs."})

    if "risk" in msg:
        return jsonify({"reply": "Risk score combines ML probability + Google Safe + AbuseIPDB."})

    if "ip" in msg:
        return jsonify({"reply": "IP shows attacker location resolved via DNS + geo APIs."})

    return jsonify({"reply": "I can help analyze URLs, risks, phishing, and security concepts."})