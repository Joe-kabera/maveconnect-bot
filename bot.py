from flask import Flask, request
import requests

TOKEN = "7988782705:AAHNIslg-MAz0PYkPcBwpqHwceCKlisrwaA"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    message = data.get("message")
    if not message:
        return "ok"

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        requests.get(URL + "sendMessage", params={
            "chat_id": chat_id,
            "text": "🚀 Maveconnect Bot is LIVE!"
        })

    return "ok"


@app.route("/")
def home():
    return "Bot running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
