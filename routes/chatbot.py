from flask import Blueprint, request, jsonify

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/", methods=["POST"])
def chat():
    msg = request.json["message"].lower()

    if "phishing" in msg:
        reply = "Phishing is a cyber attack that tricks users into revealing sensitive data."
    elif "prevent" in msg:
        reply = "Always verify URLs, avoid unknown links, and use 2FA."
    else:
        reply = "I can help explain threats and scan results."

    return jsonify({"response": reply})