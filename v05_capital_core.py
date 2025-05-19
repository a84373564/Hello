import json
import os
import requests
import hmac
import hashlib
import time
from datetime import datetime

TRACKER_PATH = "/mnt/data/hello/capital_tracker.json"
API_KEY_PATH = "/mnt/data/hello/api_keys.json"

def load_capital():
    try:
        with open(TRACKER_PATH, "r") as f:
            data = json.load(f)
            return float(data.get("current_capital", 0))
    except Exception:
        return 0

def update_capital(new_value):
    with open(TRACKER_PATH, "r") as f:
        data = json.load(f)
    data["current_capital"] = float(new_value)
    data["updated"] = datetime.now().isoformat()
    with open(TRACKER_PATH, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[Ω] 資金更新為 {new_value:.2f} USDT")

def reset_capital():
    with open(TRACKER_PATH, "r") as f:
        data = json.load(f)
    initial = float(data.get("initial_capital", 100))
    data["current_capital"] = initial
    data["updated"] = datetime.now().isoformat()
    with open(TRACKER_PATH, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[Ω] 資金重置為初始值 {initial:.2f} USDT")

def sync_wallet_from_api():
    if not os.path.exists(API_KEY_PATH):
        print("[!] 未偵測到 API 金鑰設定檔，跳過自動同步")
        return
    with open(API_KEY_PATH, "r") as f:
        keys = json.load(f)
    access_key = keys.get("access_key")
    secret_key = keys.get("secret_key")
    if not access_key or not secret_key:
        print("[!] API 金鑰未填寫，跳過同步")
        return

    url = "https://api.mexc.com/api/v3/account"
    timestamp = int(time.time() * 1000)
    params = {"timestamp": timestamp}
    query_string = '&'.join(f"{k}={v}" for k, v in sorted(params.items()))
    signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    params["signature"] = signature
    headers = {"X-MEXC-APIKEY": access_key}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            balances = response.json().get("balances", [])
            for asset in balances:
                if asset["asset"] == "USDT":
                    usdt_balance = float(asset["free"])
                    update_capital(usdt_balance)
                    return
        else:
            print("[×] 錢包 API 請求失敗：", response.status_code)
    except Exception as e:
        print("[×] 錢包同步錯誤：", str(e))

def get_risk_parameters():
    sync_wallet_from_api()  # 每次執行都會嘗試自動更新
    capital = load_capital()
    return {
        "capital": capital,
        "max_risk": round(capital * 0.03, 2),
        "position_size": round(capital * 0.1, 2),
        "min_capital": 10
    }

if __name__ == "__main__":
    print("[Ω] 當前資金：", load_capital(), "USDT")
    print("[Ω] 風控參數：", get_risk_parameters())
