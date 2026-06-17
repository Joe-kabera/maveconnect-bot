from flask import Flask, request
import requests

TOKEN = "7988782705:AAHNIslg-MAz0PYkPcBwpqHwceCKlisrwaA"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)   # 👈 MUST be here first


def send(chat_id, text):
    requests.get(URL + "sendMessage", params={
        "chat_id": chat_id,
        "text": text
    })


@app.route("/")
def home():
    return "Bot running"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
