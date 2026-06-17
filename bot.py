from flask import Flask, request
import requests
import os

TOKEN = "7988782705:AAHrQd8ZJB_W0YgP1r1BVloGTXhJnQ7r-is"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)


def send(chat_id, text):
    try:
        requests.get(
            BASE_URL + "sendMessage",
            params={
                "chat_id": chat_id,
                "text": text
            },
            timeout=10
        )
    except Exception as e:
        print("SEND ERROR:", e)


@app.route("/")
def home():
    return "Maveconnect Bot 12 is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("UPDATE:", data)

        if not data:
            return "ok"

        message = data.get("message")
        if not message:
            return "ok"

        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        if text == "/start":
            send(chat_id, "🚀 Welcome to Maveconnect!")

        elif text == "/help":
            send(chat_id, "Commands: /start /help /test")

        elif text == "/test":
            send(chat_id, "✅ Bot working")

        else:
            send(chat_id, "🤖 Command received")

    except Exception as e:
        print("ERROR:", e)

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
