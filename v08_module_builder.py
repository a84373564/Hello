# /mnt/data/hello/v08_module_builder.py
import os
import json
import random
import time

PRICE_DIR = "/mnt/data/hello/prices"
OUTPUT_DIR = "/mnt/data/hello/modules"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_price(symbol):
    path = os.path.join(PRICE_DIR, f"{symbol}.json")
    if not os.path.exists(path):
        print(f"[!] 找不到價格檔：{path}")
        return None
    with open(path, "r") as f:
        data = json.load(f)
        return data.get("price")

def generate_mutant(symbol, base_price):
    logic = {
        "symbol": symbol,
        "entry_threshold": round(random.uniform(0.01, 0.05), 4),
        "take_profit": round(random.uniform(0.03, 0.10), 4),
        "stop_loss": round(random.uniform(0.01, 0.05), 4),
        "multi_symbol": True,
        "garou_mutation": True,
        "base_price": base_price,
        "created_at": time.time()
    }
    return logic

def save_module(symbol, logic):
    filename = f"mod_{symbol}_{int(time.time())}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(logic, f, indent=2)
    print(f"[+] 已建構模組：{filepath}")

def main():
    print("[◎] 啟動 v08 模組建構器（瘋狗＋多幣模式）")
    symbols = []
    top_path = "/mnt/data/hello/top_symbols.json"
    if os.path.exists(top_path):
        with open(top_path, "r") as f:
            symbols = json.load(f)
    else:
        print("[!] 找不到 top_symbols.json，請先執行 v03")
        return

    for symbol in symbols:
        price = get_price(symbol)
        if price is None:
            continue
        logic = generate_mutant(symbol, price)
        save_module(symbol, logic)

    print("[*] 模組建構完成")

if __name__ == "__main__":
    main()
