import os
import json
import random
import string
from datetime import datetime

# === 路徑設定 ===
PRICE_DIR = "prices"
MODULE_DIR = "modules"
os.makedirs(MODULE_DIR, exist_ok=True)

# === 嘗試載入 MEXC API 金鑰（可略過不中斷） ===
try:
    with open("/mnt/data/hello/mexc_keys.json") as f:
        keys = json.load(f)
        print("[Ω] API 金鑰載入成功")
except:
    print("[!] 未偵測到 API 金鑰設定檔，跳過自動同步")
    keys = None

# === 瘋狗 Garou 交易邏輯產生器 ===
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

# === 掃描價格資料與建模 ===
today = datetime.now().strftime("%Y%m%d")
count = 0
symbols = []

if not os.path.exists(PRICE_DIR):
    print(f"[!] 價格資料夾不存在：{PRICE_DIR}")
    exit(0)

for fname in os.listdir(PRICE_DIR):
    if fname.endswith(".json"):
        symbols.append(fname.replace(".json", ""))

for sym in symbols:
    try:
        with open(os.path.join(PRICE_DIR, f"{sym}.json")) as f:
            data = json.load(f)
        if "close" not in data or not isinstance(data["close"], list):
            raise ValueError("無效或缺少 close 資料")
    except Exception as e:
        print(f"[!] 略過 {sym}，原因：{e}")
        continue

    for _ in range(5):  # 每幣產 5 支模組
        modname = f"module_{today}_{''.join(random.choices(string.digits, k=6))}_{sym}_mad.py"
        with open(os.path.join(MODULE_DIR, modname), "w") as f:
            f.write(generate_module(sym))
        print(f"[✓] 產出模組：{modname}")
        count += 1

print(f"[Ω] 本輪共產出 {count} 支模組")
