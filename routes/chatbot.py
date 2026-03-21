from flask import Blueprint, request, jsonify

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    message = request.json.get("message")

    # Simple intelligent reply
    if "phishing" in message.lower():
        reply = "Phishing sites try to steal credentials. Avoid clicking unknown links."
    elif "safe" in message.lower():
        reply = "Always verify HTTPS and domain before trusting a website."
    else:
        reply = "I can help analyze URLs and detect threats."

    return jsonify({"reply": reply})