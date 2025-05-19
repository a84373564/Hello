import os
import json
import random
import string

PRICE_DIR = "prices"
MODULE_DIR = "modules"
os.makedirs(MODULE_DIR, exist_ok=True)

# 嘗試載入金鑰
try:
    with open("/mnt/data/hello/mexc_keys.json") as f:
        keys = json.load(f)
        print("[Ω] API 金鑰載入成功")
except Exception as e:
    print("[!] 未偵測到 API 金鑰設定檔，跳過自動同步")
    keys = None

# 模組產生器（瘋狗版）
def generate_module(symbol):
    return f'''
def run(data, capital, history):
    import random
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
'''.strip()

# 掃描所有價格 JSON
symbols = []
for fname in os.listdir(PRICE_DIR):
    if fname.endswith(".json"):
        symbols.append(fname.replace(".json", ""))

count = 0
for sym in symbols:
    try:
        with open(os.path.join(PRICE_DIR, f"{sym}.json")) as f:
            data = json.load(f)
        if not isinstance(data, dict) or "close" not in data or not isinstance(data["close"], list):
            raise ValueError("close 欄位格式錯誤或不存在")
    except Exception as e:
        print(f"[!] 略過 {sym}，錯誤原因：{e}")
        continue

    for _ in range(5):
        modname = f"module_20250519_{''.join(random.choices(string.digits, k=6))}_{sym}_mad.py"
        with open(os.path.join(MODULE_DIR, modname), "w") as f:
            f.write(generate_module(sym))
        print(f"[✓] 模組儲存：{modname}")
        count += 1

print(f"[Ω] 本輪總共產出 {count} 支模組")
