import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8714844252:AAGJSCEApwfK5ws4W996MHY2XLNOUZmF4Us")
CHAT_ID = os.environ.get("CHAT_ID", "YOUR_CHAT_ID_HERE")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "Visal Portfolio Bot is running"})


@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()

    name = data.get("name", "N/A")
    telegram = data.get("telegram", "N/A")
    subject = data.get("subject", "N/A")
    message = data.get("message", "N/A")

    text = (
        f"📬 *New Contact Form Message*\n\n"
        f"👤 *Name:* {name}\n"
        f"📱 *Telegram:* {telegram}\n"
        f"📌 *Subject:* {subject}\n"
        f"💬 *Message:*\n{message}"
    )

    response = requests.post(
        TELEGRAM_URL,
        json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown",
        },
    )

    if response.status_code == 200:
        return jsonify({"status": "ok", "message": "Sent to Telegram"}), 200
    else:
        return jsonify({"status": "error", "detail": response.text}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
