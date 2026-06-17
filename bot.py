from flask import Flask, request
import requests
import os

# ===== BOT CONFIG =====
TOKEN = "7988782705:AAHNIslg-MAz0PYkPcBwpqHwceCKlisrwaA"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

# ===== TELEGRAM SEND FUNCTION =====
def send(chat_id, text):
    try:
        response = requests.get(
            URL + "sendMessage",
            params={
                "chat_id": chat_id,
                "text": text
            }
        )

        print("SendMessage status:", response.status_code)
        print("SendMessage response:", response.text)

    except Exception as e:
        print("Send error:", e)


# ===== HOME ROUTE =====
@app.route("/")
def home():
    return "Maveconnect Bot is running!"


# ===== WEBHOOK ROUTE =====
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        print("🔥 UPDATE:", data)

        if not data:
            return "ok"

        message = data.get("message")

        if not message:
            return "ok"

        chat_id = message["chat"]["id"]
        text = message.get("text", "")

        print("📩 TEXT:", text)

        # START
        if text == "/start":
            send(
                chat_id,
                "🚀 Welcome to Maveconnect Bot!\n\n"
                "Available commands:\n"
                "/help\n"
                "/test"
            )

        # HELP
        elif text == "/help":
            send(
                chat_id,
                "📋 Commands:\n"
                "/start - Start bot\n"
                "/help - Show help\n"
                "/test - Test bot"
            )

        # TEST
        elif text == "/test":
            send(chat_id, "✅ Test successful")

        else:
            send(
                chat_id,
                "🤖 Command received.\n"
                "Use /help to see available commands."
            )

    except Exception as e:
        print("❌ ERROR:", e)

    return "ok"


# ===== START SERVER =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
