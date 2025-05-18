import ccxt
import json

def get_top_symbols(limit=3):
    with open("mexc_keys.json", "r") as f:
        keys = json.load(f)

    exchange = ccxt.mexc({
        'apiKey': keys['apiKey'],
        'secret': keys['secret'],
        'enableRateLimit': True
    })

    markets = exchange.load_markets()
    symbols = []

    for symbol in markets:
        market = markets[symbol]
        if not market['active'] or not symbol.endswith('/USDT'):
            continue
        try:
            ticker = exchange.fetch_ticker(symbol)
            volume_usd = ticker['baseVolume'] * ticker['last']
            price_range = (ticker['high'] - ticker['low']) / ticker['low'] if ticker['low'] > 0 else 0
            if volume_usd > 1000000 and price_range > 0.03:
                symbols.append((symbol.replace("/", ""), volume_usd, price_range))
        except Exception:
            continue

    symbols.sort(key=lambda x: (x[1], x[2]), reverse=True)
    top = [s[0] for s in symbols[:limit]]

    with open("top_symbols.json", "w") as f:
        json.dump(top, f)

    print(f"[Ω] 已選出熱門幣種：{top}")

if __name__ == "__main__":
    get_top_symbols()
