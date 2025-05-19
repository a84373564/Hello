# /mnt/data/hello/v03_symbol_screener_omega.py
import ccxt
import json
import os
import traceback

KEY_PATH = "/mnt/data/hello/mexc_keys.json"
PRICE_DIR = "/mnt/data/hello/prices"
TOP_LIMIT = 5  # 可自調最多下載幣數

os.makedirs(PRICE_DIR, exist_ok=True)

def get_keys():
    try:
        with open(KEY_PATH, "r") as f:
            keys = json.load(f)
        return keys["apiKey"], keys["api_secret"]
    except Exception as e:
        print(f"[!] 金鑰讀取失敗：{e}")
        return None, None

def get_top_symbols(limit=TOP_LIMIT):
    api_key, api_secret = get_keys()
    if not api_key or not api_secret:
        return []

    exchange = ccxt.mexc({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True
    })

    try:
        markets = exchange.load_markets()
    except Exception as e:
        print(f"[!] 無法載入市場資料：{e}")
        return []

    symbols = []
    for symbol in markets:
        market = markets[symbol]
        if not market['active'] or not symbol.endswith('/USDT'):
            continue
        try:
            ticker = exchange.fetch_ticker(symbol)
            volume_usd = ticker['baseVolume'] * ticker['last']
            price_range = (ticker['high'] - ticker['low']) / ticker['low'] if ticker['low'] > 0 else 0
            if volume_usd > 1_000_000 and price_range > 0.03:
                symbols.append((symbol.replace("/", ""), volume_usd, price_range))
        except Exception:
            continue

    symbols.sort(key=lambda x: (x[1], x[2]), reverse=True)
    return [s[0] for s in symbols[:limit]]

def download_price(symbol):
    try:
        url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        result = [{"close": float(c[4])} for c in data]
        with open(f"{PRICE_DIR}/{symbol}.json", "w") as f:
            json.dump(result, f)
        print(f"[✓] 價格下載完成：{symbol}")
    except Exception as e:
        print(f"[!] 價格下載錯誤 {symbol}：{e}")

def main():
    print("[Ω] 啟動 v03 幣種偵測器（終極強化版）")
    symbols = get_top_symbols()
    if not symbols:
        print("[!] 無可用幣種，略過")
        return
    for sym in symbols:
        download_price(sym)
    print(f"[Ω] 幣種與價格完成：{len(symbols)} 種")

if __name__ == "__main__":
    import requests
    main()
