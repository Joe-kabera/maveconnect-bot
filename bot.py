from flask import Flask, request
import requests
import os

TOKEN = "7988782705:AAFS9c5D_v-o15b5hBJZmNXW4aol4BgtUf4"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(name)

=====================

SEND MESSAGE

=====================

def send(chat_id, text):
try:
response = requests.get(
BASE_URL + "sendMessage",
params={
"chat_id": chat_id,
"text": text
},
timeout=10
)
print("SEND STATUS:", response.status_code)
print("SEND RESPONSE:", response.text)

except Exception as e:
    print("SEND ERROR:", e)

=====================

GET CRYPTO PRICE

=====================

def get_price(symbol):
symbol = symbol.lower()

mapping = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "bnb": "binancecoin",
    "xrp": "ripple"
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

    print("API STATUS:", response.status_code)

    data = response.json()

    print("COINGECKO DATA:", data)

    if coin in data:
        return data[coin]["usd"]

    return None

except Exception as e:
    print("PRICE ERROR:", e)
    return None

=====================

HOME

=====================

@app.route("/")
def home():
return "Maveconnect Bot is running!"

=====================

WEBHOOK

=====================

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

    print("TEXT:", text)

    # START
    if text == "/start":
        send(chat_id, "🚀 Welcome to Maveconnect Bot!")

    # HELP
    elif text == "/help":
        send(
            chat_id,
            "Commands:\n"
            "/start\n"
            "/help\n"
            "/test\n"
            "/btc btc\n"
            "/btc eth"
        )

    # TEST
    elif text == "/test":
        send(chat_id, "✅ Bot working")

    # PRICE COMMAND
    elif text.lower().startswith("/btc"):

        parts = text.split()

        print("PARTS:", parts)

        if len(parts) < 2:
            send(chat_id, "Usage: /btc BTC")
        else:
            symbol = parts[1]

            print("SYMBOL:", symbol)

            price = get_price(symbol)

            print("PRICE:", price)

            if price is not None:
                send(
                    chat_id,
                    f"💰 {symbol.upper()} Price: ${price}"
                )
            else:
                send(
                    chat_id,
                    "❌ Price unavailable or coin unsupported."
                )

    else:
        send(chat_id, "🤖 Command not recognized")

except Exception as e:
    print("WEBHOOK ERROR:", e)

return "ok"

if name == "main":
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
