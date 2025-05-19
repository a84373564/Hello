import os
import json
import requests
import time

KEY_PATH = "/mnt/data/hello/mexc_keys.json"
PRICE_DIR = "/mnt/data/hello/prices"
TOP_LIMIT = 3  # 同時最多抓幾種幣

os.makedirs(PRICE_DIR, exist_ok=True)

def get_keys():
    try:
        with open(KEY_PATH, "r") as f:
            keys = json.load(f)
        return keys["api_key"], keys["api_secret"]
    except Exception as e:
        print(f"[!] 載入 API 金鑰失敗：{e}")
        return None, None

def get_top_symbols():
    try:
        resp = requests.get("https://api.mexc.com/api/v3/ticker/24hr", timeout=10)
        data = resp.json()
        ranked = sorted(
            [d for d in data if d["symbol"].endswith("USDT")],
            key=lambda x: float(x.get("quoteVolume", 0)),
            reverse=True
        )
        return [r["symbol"] for r in ranked[:TOP_LIMIT]]
    except Exception as e:
        print(f"[!] 無法取得幣種列表：{e}")
        return []

def download_price(symbol):
    try:
        url = f"https://api.mexc.com/api/v3/klines?symbol={symbol}&interval=1h&limit=100"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        result = [{"close": float(c[4])} for c in data]
        with open(f"{PRICE_DIR}/{symbol}.json", "w") as f:
            json.dump(result, f)
        print(f"[✓] 已下載：{symbol}")
    except Exception as e:
        print(f"[!] 下載價格失敗 {symbol}：{e}")

def main():
    print("[Ω] 啟動 v03 幣種偵測器（強化版）")
    symbols = get_top_symbols()
    if not symbols:
        print("[!] 無可用幣種，略過")
        return
    for sym in symbols:
        download_price(sym)
    print(f"[Ω] 幣種與價格下載完成：{len(symbols)} 種")

if __name__ == "__main__":
    main()
