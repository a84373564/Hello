import os
import json
import random
import string
from datetime import datetime

PRICE_DIR = "prices"
MODULE_DIR = "modules"
os.makedirs(MODULE_DIR, exist_ok=True)

def generate_module(symbol):
    code = f"""
def run(data, capital, history):
    log = []
    holding = False
    position_size = 0.1
    min_capital = 10

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

today = datetime.now().strftime("%Y%m%d")
count = 0

for fname in os.listdir(PRICE_DIR):
    if not fname.endswith(".json"):
        continue
    symbol = fname.replace(".json", "")
    try:
        with open(os.path.join(PRICE_DIR, fname)) as f:
            data = json.load(f)
            if "close" not in data:
                raise ValueError("缺少 close 資料")
    except Exception as e:
        print(f"[!] 略過 {symbol}，原因：{e}")
        continue

    for _ in range(5):  # 每個幣種產 5 支模組
        modname = f"module_{today}_{''.join(random.choices(string.digits, k=6))}_{symbol}_mad.py"
        with open(os.path.join(MODULE_DIR, modname), "w") as f:
            f.write(generate_module(symbol))
        print(f"[✓] 產出模組：{modname}")
        count += 1

print(f"[Ω] 本輪共產出 {count} 支模組")
