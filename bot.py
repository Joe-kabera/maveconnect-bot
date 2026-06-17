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
            send(chat_id, "🚀 Bot is working!")

        # TEST RAW RESPONSE
        elif text == "/test":
            send(chat_id, "✅ Test successful")

        else:
            send(chat_id, "🤖 Command received but not recognized")

    except Exception as e:
        print("❌ ERROR:", e)

    return "ok"
