import json
import os
import time
import hmac
import hashlib
import requests

KEY_PATH = "/mnt/data/hello/mexc_keys.json"
OUTPUT_PATH = "/mnt/data/hello/capital_tracker.json"

def load_capital():
    if not os.path.exists(OUTPUT_PATH):
        return 100
    with open(OUTPUT_PATH, "r") as f:
        return json.load(f).get("current_capital", 100)

def update_capital(new_value):
    info = {
        "current_capital": round(new_value, 2),
        "initial_capital": 100,
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(info, f, indent=2)
    print(f"[✓] 資金已更新為：{new_value} USDT")

def reset_capital():
    update_capital(100)

def load_keys():
    if not os.path.exists(KEY_PATH):
        print("[!] 找不到 API 金鑰檔案：mexc_keys.json")
        return None, None
    with open(KEY_PATH, "r") as f:
        key_data = json.load(f)
    return key_data.get("api_key"), key_data.get("api_secret")

def sign_request(api_key, api_secret, recv_window="5000"):
    timestamp = str(int(time.time() * 1000))
    query = f"timestamp={timestamp}&recvWindow={recv_window}"
    signature = hmac.new(api_secret.encode(), query.encode(), hashlib.sha256).hexdigest()
    headers = {
        "X-MEXC-APIKEY": api_key
    }
    return query + f"&signature={signature}", headers

def sync_wallet_from_api():
    print("[◎] 正在同步 MEXC 錢包資金...")
    api_key, api_secret = load_keys()
    if not api_key or not api_secret:
        print("[!] API 金鑰錯誤或缺失")
        return

    endpoint = "https://api.mexc.com/api/v3/account"
    query_string, headers = sign_request(api_key, api_secret)
    url = f"{endpoint}?{query_string}"

    print(f"[→] 發送請求 URL：{url}")

    try:
        resp = requests.get(url, headers=headers)
        print(f"[←] 狀態碼：{resp.status_code}")
        data = resp.json()
        print(f"[←] 回傳內容：{json.dumps(data, indent=2)}")

        for asset in data.get("balances", []):
            if asset["asset"] == "USDT":
                usdt_amt = float(asset["free"]) + float(asset["locked"])
                update_capital(usdt_amt)
                return

        print("[!] 找不到 USDT 餘額")
    except Exception as e:
        print(f"[!] 錢包同步失敗：{e}")
