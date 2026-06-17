@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if not text:
        return "ok"

    parts = text.split()
    command = parts[0]

    try:

        # START
        if command == "/start":
            send(chat_id, "🚀 Maveconnect Bot is LIVE")

        # HELP
        elif command == "/help":
            send(chat_id, "Commands: /price BTC, /analyze btc, /ai btc")

        # PRICE
        elif command == "/price":
            if len(parts) < 2:
                send(chat_id, "❌ Usage: /price BTC")
            else:
                symbol = parts[1]
                price = get_price(symbol)
                send(chat_id, f"💰 {symbol.upper()} = ${price}")

        # ANALYZE
        elif command == "/analyze":
            if len(parts) < 2:
                send(chat_id, "❌ Usage: /analyze bitcoin")
            else:
                symbol = parts[1]
                data = analyze_market(symbol)
                send(chat_id, ai_analysis(data, symbol))

        # AI
        elif command == "/ai":
            if len(parts) < 2:
                send(chat_id, "❌ Usage: /ai btc")
            else:
                symbol = parts[1]
                data = analyze_market(symbol)
                send(chat_id, ai_analysis(data, symbol))

        # GAME
        elif command == "/game":
            action = parts[1] if len(parts) > 1 else "start"
            send(chat_id, platypus_game(chat_id, action))

    except Exception as e:
        print("ERROR:", e)
        send(chat_id, "⚠️ Bot error occurred")

    return "ok"
