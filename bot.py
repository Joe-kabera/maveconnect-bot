from flask import Flask, request
import requests
import os

TOKEN = "7988782705:AAEGbPteBY3V0l1Abp9ZNO8Y3TMQk5Zjz5U"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)


# =====================
# SEND MESSAGE FUNCTION
# =====================
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


# =====================
# PRICE FUNCTION
# =====================
def get_price(symbol):
    symbol = symbol.lower()

    mapping = {
        "btc": "bitcoin",
        "eth": "ethereum"
    }

    coin = mapping.get(symbol)
    if not coin:
        return None

    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": coin,
            "vs_currencies": "usd"
        }

        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        print("COINGECKO RESPONSE:", data)

        return data.get(coin, {}).get("usd")

    except Exception as e:
        print("PRICE ERROR:", e)
        return None


# =====================
# HOME ROUTE
# =====================
@app.route("/")
def home():
    return "Maveconnect Bot 12 is running!"


# =====================
# WEBHOOK ROUTE
# =====================
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

        # START
        if text == "/start":
            send(chat_id, "🚀 Welcome to Maveconnect Bot!")

        # HELP
        elif text == "/help":
            send(chat_id, "Commands: /start /help /test /btc BTC")

        # TEST
        elif text == "/test":
            send(chat_id, "✅ Bot working")

        # BTC PRICE
        elif text.startswith("/btc"):
            parts = text.split()

            if len(parts) < 2:
                send(chat_id, "Usage: /btc BTC")
            else:
                price = get_price(parts[1])

                if price:
                    send(chat_id, f"💰 Price: ${price}")
                else:
                    send(chat_id, "Coin not supported")

        else:
            send(chat_id, "🤖 Command not recognized")

    except Exception as e:
        print("ERROR:", e)

    return "ok"


# =====================
# RUN SERVER
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
