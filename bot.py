from flask import Flask, request
import requests
import os

# =====================
# CONFIG
# =====================
TOKEN = "7988782705:AAFS9c5D_v-o15b5hBJZmNXW4aol4BgtUf4"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)


# =====================
# SEND MESSAGE
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
# PRICE FUNCTION (STABLE VERSION)
# =====================
def get_price(symbol):
    symbol = symbol.lower().strip()

    mapping = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "sol": "solana",
        "bnb": "binancecoin",
        "xrp": "ripple",
        "ada": "cardano",
        "doge": "dogecoin",
        "ltc": "litecoin",
        "dot": "polkadot"
    }

    coin = mapping.get(symbol)

    if not coin:
        print("UNSUPPORTED COIN:", symbol)
        return None

    try:
        url = "https://api.coingecko.com/api/v3/simple/price"

        response = requests.get(
            url,
            params={
                "ids": coin,
                "vs_currencies": "usd"
            },
            timeout=10
        )

        print("STATUS CODE:", response.status_code)

        if response.status_code != 200:
            print("API ERROR:", response.text)
            return None

        data = response.json()
        print("COINGECKO RESPONSE:", data)

        if not isinstance(data, dict):
            return None

        if coin not in data:
            return None

        return data[coin].get("usd")

    except Exception as e:
        print("PRICE ERROR:", e)
        return None


# =====================
# HOME ROUTE
# =====================
@app.route("/")
def home():
    return "Maveconnect Bot is running!"


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

        message = data.get("message") or data.get("edited_message")

        if not message:
            return "ok"

        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip()

        print("TEXT:", text)

        # START
        if text == "/start":
            send(chat_id, "🚀 Welcome to Maveconnect Crypto Bot!")

        # HELP
        elif text == "/help":
            send(
                chat_id,
                "Commands:\n"
                "/start\n"
                "/help\n"
                "/test\n"
                "/btc btc\n"
                "/btc eth\n"
                "/btc sol"
            )

        # TEST
        elif text == "/test":
            send(chat_id, "✅ Bot is working!")

        # PRICE CHECK
        elif text.lower().startswith("/btc"):
            parts = text.split()

            if len(parts) < 2:
                send(chat_id, "Usage: /btc BTC")
                return "ok"

            symbol = parts[1]
            price = get_price(symbol)

            print("FINAL PRICE:", price)

            if price is not None:
                send(chat_id, f"💰 {symbol.upper()} Price: ${price}")
            else:
                send(chat_id, "⚠️ Price temporarily unavailable. Try again.")

        else:
            send(chat_id, "🤖 Unknown command. Use /help")

    except Exception as e:
        print("WEBHOOK ERROR:", e)

    return "ok"


# =====================
# RUN SERVER (RENDER)
# =====================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
