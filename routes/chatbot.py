from flask import Blueprint, request, jsonify
from services.chatbot_engine import ChatbotEngine

chatbot_bp = Blueprint("chatbot", __name__)
_bot = ChatbotEngine()


@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    context = data.get("context") or {}

    if not message:
        return jsonify({"error": "Message is required"}), 400

    response = _bot.respond(message, context)
    return jsonify({"response": response}), 200
