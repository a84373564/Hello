import requests
import json
import hmac
import hashlib
import time

API_KEY_PATH = "/mnt/data/hello/api_keys.json"
TRACKER_PATH = "/mnt/data/hello/capital_tracker.json"

def load_keys():
    with open(API_KEY_PATH, "r") as f:
        keys = json.load(f)
    return keys["access_key"], keys["secret_key"]

def sign_request(params, secret_key):
    sorted_params = sorted(params.items())
    query_string = '&'.join(f"{k}={v}" for k, v in sorted_params)
    signature = hmac.new(secret_key.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    return signature

def fetch_usdt_balance(access_key, secret_key):
    url = "https://api.mexc.com/api/v3/account"
    timestamp = int(time.time() * 1000)
    params = {
        "timestamp": timestamp
    }
    signature = sign_request(params, secret_key)
    headers = {
        "X-MEXC-APIKEY": access_key
    }
    params["signature"] = signature
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        balances = response.json().get("balances", [])
        for asset in balances:
            if asset["asset"] == "USDT":
                return float(asset["free"])
    else:
        print("API 錯誤：", response.status_code, response.text)
    return None

def update_tracker(usdt_balance):
    tracker = {
        "initial_capital": usdt_balance,
        "current_capital": usdt_balance,
        "updated": time.strftime("%Y-%m-%dT%H:%M:%S")
    }
    with open(TRACKER_PATH, "w") as f:
        json.dump(tracker, f, indent=2)
    print(f"[✓] 已更新 tracker（USDT: {usdt_balance}）")

def main():
    access_key, secret_key = load_keys()
    usdt = fetch_usdt_balance(access_key, secret_key)
    if usdt is not None:
        update_tracker(usdt)
    else:
        print("[×] 無法獲得錢包資訊")

if __name__ == "__main__":
    main()
