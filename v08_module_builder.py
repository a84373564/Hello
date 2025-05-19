import os
import json
import random
import string

PRICE_DIR = "prices"
MODULE_DIR = "modules"
os.makedirs(MODULE_DIR, exist_ok=True)

try:
    with open("/mnt/data/hello/mexc_keys.json") as f:
        keys = json.load(f)
        print("[Ω] API 金鑰載入成功")
except Exception:
    print("[!] 未偵測到 API 金鑰設定檔，跳過自動同步")
    keys = None

def generate_module(symbol):
    code = f"""
import random

def run(data, capital, history):
    log = []
    holding = False
    min_capital = 10
    position_size = 0.1

    for i in range(len(data["close"])):
        price = data["close"][i]
        if i % 5 == 0 and not holding:
            if capital >= min_capital:
                capital -= price * position_size
                log.append(f"Buy at {{price:.2f}}")
                holding = True
        elif i % 5 == 3 and holding:
            capital += price * position_size
            log.append(f"Sell at {{price:.2f}}")
            holding = False

    return {{
        "log": log,
        "score": random.uniform(-50, 50),
        "symbol": "{symbol}"
    }}
"""
    return code.strip()

symbols = []
for fname in os.listdir(PRICE_DIR):
    if not fname.endswith(".json"):
        continue

    symbol = fname.replace(".json", "")
    fpath = os.path.join(PRICE_DIR, fname)

    try:
        with open(fpath, "r") as f:
            data = json.load(f)
        if "close" not in data and isinstance(data, list):
            data = {"close": data}
            with open(fpath, "w") as f:
                json.dump(data, f)
        if "close" in data and isinstance(data["close"], list) and len(data["close"]) > 10:
            symbols.append(symbol)
    except Exception as e:
        print(f"[!] 無法讀取 {fname}：{e}")

count = 0
for sym in symbols:
    for _ in range(5):
        name = f"module_20250519_{''.join(random.choices(string.digits, k=6))}_{sym}_mad.py"
        path = os.path.join(MODULE_DIR, name)
        with open(path, "w") as f:
            f.write(generate_module(sym))
        print(f"[✓] 模組儲存：{name}")
        count += 1

print(f"[Ω] 本輪總共產出 {count} 支模組")
