import threading
import requests
import time
import os
from flask import Flask

TOKEN = "7988782705:AAHNIslg-MAz0PYkPcBwpqHwceCKlisrwaA"
URL = f"https://api.telegram.org/bot{TOKEN}/"

app = Flask(__name__)

last_update_id = None

def bot_loop():
    global last_update_id

    while True:
        try:
            r = requests.get(URL + "getUpdates", params={"offset": last_update_id})
            data = r.json()

            for update in data.get("result", []):
                last_update_id = update["update_id"] + 1

                message = update.get("message")
                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text == "/start":
                    requests.get(URL + "sendMessage", params={
                        "chat_id": chat_id,
                        "text": "🚀 Maveconnect Bot is LIVE!"
                    })

                elif text == "/help":
                    requests.get(URL + "sendMessage", params={
                        "chat_id": chat_id,
                        "text": "Commands: /start /help"
                    })

            time.sleep(2)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

@app.route("/")
def home():
    return "Maveconnect Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=bot_loop, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
