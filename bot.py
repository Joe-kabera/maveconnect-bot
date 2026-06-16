import requests
import time

TOKEN = "7988782705:AAHNIslg-MAz0PYkPcBwpqHwceCKlisrwaA"
URL = f"https://api.telegram.org/bot{TOKEN}/"

last_update_id = None

def send_message(chat_id, text):
    requests.get(URL + "sendMessage", params={
        "chat_id": chat_id,
        "text": text
    })

def get_updates():
    global last_update_id
    r = requests.get(URL + "getUpdates", params={"offset": last_update_id})
    return r.json()

print("Maveconnect Bot is running...")

while True:
    try:
        data = get_updates()

        for update in data.get("result", []):
            last_update_id = update["update_id"] + 1

            message = update.get("message")
            if not message:
                continue

            chat_id = message["chat"]["id"]
            text = message.get("text", "")

            if text == "/start":
                send_message(chat_id, "🚀 Maveconnect Bot is LIVE on cloud!")
            elif text == "/help":
                send_message(chat_id, "Commands:\n/start\n/help")
            else:
                send_message(chat_id, "Unknown command")

        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
