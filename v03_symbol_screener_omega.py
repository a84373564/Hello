import ccxt
import json
import time

def get_top_symbols(limit=3):
    with open("mexc_keys.json", "r") as f:
        keys = json.load(f)

    exchange = ccxt.mexc({
        'apiKey': keys['apiKey'],
        'secret': keys['secret'],
        'enableRateLimit': True,
        'timeout': 10000  # 10 秒 timeout
    })

    markets = exchange.load_markets()
    symbols = []

    print(f"[啟動] 篩選幣種中，請稍候...")

    for idx, symbol in enumerate(markets):
        market = markets[symbol]
        if not market['active'] or not symbol.endswith('/USDT'):
            continue
        try:
            ticker = exchange.fetch_ticker(symbol)
            volume_usd = ticker['baseVolume'] * ticker['last']
            price_range = (ticker['high'] - ticker['low']) / ticker['low'] if ticker['low'] > 0 else 0
            if volume_usd > 1_000_000 and price_range > 0.03:
                symbols.append((symbol.replace("/", ""), volume_usd, price_range))
            if idx % 20 == 0:
                print(f"檢查中：{idx} / {len(markets)}")
        except Exception as e:
            continue

    symbols.sort(key=lambda x: (x[1], x[2]), reverse=True)
    top = [s[0] for s in symbols[:limit]]

    with open("top_symbols.json", "w") as f:
        json.dump(top, f)

    print(f"[Ω] 熱門幣種：{top}")

if __name__ == "__main__":
    get_top_symbols()
