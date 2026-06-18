def get_price(symbol):
    symbol = symbol.lower().strip()

    # Binance symbols (faster API)
    binance_map = {
        "btc": "BTCUSDT",
        "eth": "ETHUSDT",
        "sol": "SOLUSDT",
        "bnb": "BNBUSDT",
        "xrp": "XRPUSDT",
        "ada": "ADAUSDT",
        "doge": "DOGEUSDT",
        "ltc": "LTCUSDT",
        "dot": "DOTUSDT"
    }

    pair = binance_map.get(symbol)

    # -------------------------
    # 1. TRY BINANCE FIRST
    # -------------------------
    try:
        url = f"https://api.binance.com/api/v3/ticker/price"
        r = requests.get(url, params={"symbol": pair}, timeout=8)

        data = r.json()
        print("BINANCE RESPONSE:", data)

        if "price" in data:
            return float(data["price"])

    except Exception as e:
        print("BINANCE ERROR:", e)

    # -------------------------
    # 2. FALLBACK (COINGECKO)
    # -------------------------
    fallback_map = {
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

    coin = fallback_map.get(symbol)

    if not coin:
        return None

    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        r = requests.get(
            url,
            params={"ids": coin, "vs_currencies": "usd"},
            timeout=8
        )

        data = r.json()
        print("COINGECKO RESPONSE:", data)

        return data.get(coin, {}).get("usd")

    except Exception as e:
        print("COINGECKO ERROR:", e)
        return None
