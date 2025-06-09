from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# === Load environment variables ===
load_dotenv()
app = Flask(__name__)

# === Import Mode Logic Files ===
from general_chat import general_chat_response
from home_assistant import home_assistant_response
from recipe_assistant import recipe_chat_response
from shopping_categorizer import categorize_items

# === Simple Smart Intent Detector ===
def detect_mode(user_input: str) -> str:
    user_input = user_input.lower()
    if any(word in user_input for word in ["lamp", "light", "turn on", "turn off", "door", "fan", "air", "status"]):
        return "home_assistant"
    elif any(word in user_input for word in ["recipe", "cook", "how to make", "ingredients", "dish", "meal"]):
        return "recipe_assistant"
    elif any(word in user_input for word in ["shopping", "buy", "need", "list", "grocery", "groceries"]):
        return "shopping_categorizer"
    else:
        return "general"

# === POST API Endpoint ===
@app.route('/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        user_input = data.get("message", "").strip()
        chat_history = data.get("chat_history", [])

        if user_input.lower() in ["exit", "bye", "clear chat"]:
            return jsonify({"reply": "Chat session cleared."})

        mode = detect_mode(user_input)

        if mode == "home_assistant":
            reply = home_assistant_response(user_input)
        elif mode == "recipe_assistant":
            reply = recipe_chat_response(user_input, chat_history)
        elif mode == "shopping_categorizer":
            reply = categorize_items(user_input)
        else:
            reply = general_chat_response(user_input)

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === GET version for browser testing ===
@app.route('/chat', methods=['GET'])
def chat_api_get():
    user_input = request.args.get("msg", "").strip()

    if not user_input:
        return "❌ Please provide a message using '?msg=your question' in the URL."

    mode = detect_mode(user_input)

    if mode == "home_assistant":
        reply = home_assistant_response(user_input)
    elif mode == "recipe_assistant":
        reply = recipe_chat_response(user_input, [])
    elif mode == "shopping_categorizer":
        reply = categorize_items(user_input)
    else:
        reply = general_chat_response(user_input)

    return f"🤖 Bot: {reply}"

# === Root welcome message ===
@app.route("/", methods=["GET"])
def index():
    return "✅ Hello, this is the Leap Home Assistant API. Use /chat endpoint with POST requests, or test GET using ?msg="


if __name__ == '__main__':
    app.run(debug=True)
