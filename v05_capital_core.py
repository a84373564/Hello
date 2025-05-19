import os
import json
import time
import hmac
import hashlib
import requests
from datetime import datetime

KEY_PATH = "/mnt/data/hello/mexc_keys.json"
CAPITAL_PATH = "/mnt/data/hello/capital_tracker.json"

def update_capital(usdt_amt):
    data = {
        "initial_capital": usdt_amt,
        "current_capital": usdt_amt,
        "updated": datetime.utcnow().isoformat()
    }
    with open(CAPITAL_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[✓] 資金更新完成：{usdt_amt} USDT 寫入 {CAPITAL_PATH}")

def load_keys():
    if not os.path.exists(KEY_PATH):
        print("[!] 找不到金鑰檔案")
        return None, None
    try:
        with open(KEY_PATH, "r") as f:
            data = json.load(f)
        return data.get("apiKey"), data.get("api_secret")
    except Exception as e:
        print(f"[!] JSON 金鑰解析失敗：{e}")
        return None, None

def sign_request(api_key, api_secret, recv_window="5000"):
    timestamp = str(int(time.time() * 1000))
    query = f"timestamp={timestamp}&recvWindow={recv_window}"
    signature = hmac.new(
        api_secret.encode(), query.encode(), hashlib.sha256
    ).hexdigest()
    headers = {"X-MEXC-APIKEY": api_key}
    return query + f"&signature={signature}", headers

def sync_wallet_from_api():
    print("[◎] 正在同步 MEXC 錢包資金...")
    api_key, api_secret = load_keys()
    if not api_key or not api_secret:
        print("[x] 金鑰載入失敗")
        return

    endpoint = "https://api.mexc.com/api/v3/account"
    query_string, headers = sign_request(api_key, api_secret)
    url = f"{endpoint}?{query_string}"

    print(f"[→] 發送 URL：{url}")
    try:
        resp = requests.get(url, headers=headers)
        print(f"[←] 回應狀態：{resp.status_code}")
        data = resp.json()
        print(f"[←] 回應資料：{json.dumps(data, indent=2)}")

        for asset in data.get("balances", []):
            if asset.get("asset") == "USDT":
                usdt_amt = float(asset["free"]) + float(asset["locked"])
                update_capital(usdt_amt)
                return
        print("[!] 找不到 USDT 餘額")
    except Exception as e:
        print(f"[!] 錢包同步失敗：{e}")

if __name__ == "__main__":
    sync_wallet_from_api()
