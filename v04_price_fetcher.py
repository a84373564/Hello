import ccxt
import json
import os
from datetime import datetime

def fetch_price_history(symbol, limit=300):
    exchange = ccxt.mexc()
    since = exchange.milliseconds() - limit * 60 * 60 * 1000  # limit 小時前
    try:
        ohlcv = exchange.fetch_ohlcv(symbol + "/USDT", timeframe='1h', since=since, limit=limit)
        return [
            {"time": datetime.utcfromtimestamp(c[0] / 1000).isoformat(), "open": c[1], "high": c[2], "low": c[3], "close": c[4], "volume": c[5]}
            for c in ohlcv
        ]
    except Exception as e:
        print(f"[Ω] 無法抓取 {symbol}：{e}")
        return []

def main():
    if not os.path.exists("top_symbols.json"):
        print("[Ω] 找不到 top_symbols.json，請先執行 v03_symbol_screener_omega.py")
        return

    with open("top_symbols.json", "r") as f:
        symbols = json.load(f)

    os.makedirs("prices", exist_ok=True)

    for s in symbols:
        print(f"[Ω] 抓取 {s} 的歷史價格中...")
        data = fetch_price_history(s.replace("USDT", ""))
        with open(f"prices/price_{s}.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"[Ω] {s} 完成，共 {len(data)} 筆資料")

if __name__ == "__main__":
    main()
