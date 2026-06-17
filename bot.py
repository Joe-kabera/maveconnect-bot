  from flask import Flask, request
import requests
import os

=========================

TELEGRAM CONFIG

=========================

TOKEN = "7988782705:AAHrQd8ZJB_W0YgP1r1BVloGTXhJnQ7r-is"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(name)

=========================

TELEGRAM HELPER

=========================

def send(chat_id, text):
try:
r = requests.get(
BASE_URL + "sendMessage",
params={
"chat_id": chat_id,
"text": text
},
timeout=10
)

    print("Send status:", r.status_code)
    print("Send response:", r.text)

except Exception as e:
    print("SEND ERROR:", e)

=========================

HOME ROUTE

=========================

@app.route("/")
def home():
return "Maveconnect Bot 12 is running!"

=========================

WEBHOOK ROUTE

=========================

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
    text = message.get("text", "").strip()

    print("📩 TEXT:", text)

    # START
    if text == "/start":
        send(
            chat_id,
            "🚀 Welcome to Maveconnect!\n\n"
            "Commands:\n"
            "/help\n"
            "/test\n"
            "/price BTC"
        )

    # HELP
    elif text == "/help":
        send(
            chat_id,
            "📋 Available Commands:\n"
            "/start\n"
            "/help\n"
            "/test\n"
            "/price BTC"
        )

    # TEST
    elif text == "/test":
        send(chat_id, "✅ Bot is responding correctly.")

    # PRICE (placeholder)
    elif text.lower().startswith("/price"):
        send(chat_id, "💰 Price feature coming next.")

    else:
        send(chat_id, "🤖 Command received. Use /help.")

except Exception as e:
    print("❌ ERROR:", e)

return "ok"

=========================

START SERVER

=========================

if name == "main":
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
