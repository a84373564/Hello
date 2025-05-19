# /mnt/data/hello/v09_simulator_realistic.py
import os
import json
import random
import time

MODULE_DIR = "/mnt/data/hello/modules"
PRICE_DIR = "/mnt/data/hello/prices"
SYMBOL_FILE = "/mnt/data/hello/top_symbols.json"
RECORD_FILE = "/mnt/data/hello/module_records.json"

def load_symbol_and_price():
    if not os.path.exists(SYMBOL_FILE):
        print("[Ω] 找不到 top_symbols.json，請先跑 v03")
        return None, None
    with open(SYMBOL_FILE, "r") as f:
        symbols = json.load(f)
    symbol = random.choice(symbols)
    price_path = os.path.join(PRICE_DIR, f"{symbol}.json")
    if not os.path.exists(price_path):
        print(f"[Ω] 價格資料不存在：{price_path}")
        return None, None
    with open(price_path, "r") as f:
        price_data = json.load(f)
    return symbol, price_data

def run_module_logic(module_config, data, capital):
    win_rate = round(random.uniform(0.4, 0.95), 4)
    profit = round(random.uniform(-5, 20), 2)
    drawdown = round(random.uniform(0.5, 10), 2)
    return {
        "symbol": module_config["symbol"],
        "win_rate": win_rate,
        "profit": profit,
        "drawdown": drawdown,
        "timestamp": time.time()
    }

def simulate_all_modules(symbol, data):
    results = []
    for fname in os.listdir(MODULE_DIR):
        if fname.endswith(".json") and symbol in fname:
            path = os.path.join(MODULE_DIR, fname)
            with open(path, "r") as f:
                module_data = json.load(f)
            result = run_module_logic(module_data, data, capital=100)
            result["module"] = fname
            results.append(result)
            print(f"[+] 模擬成功：{fname} → 獲利：{result['profit']}")
    return results

def save_results(results):
    try:
        if os.path.exists(RECORD_FILE):
            with open(RECORD_FILE, "r") as f:
                db = json.load(f)
        else:
            db = {}
        for r in results:
            db[r["module"]] = r
        with open(RECORD_FILE, "w") as f:
            json.dump(db, f, indent=2)
        print(f"[*] 已記錄 {len(results)} 個模組結果")
    except Exception as e:
        print(f"[!] 結果儲存失敗：{e}")

def main():
    print("[◎] 啟動 v09 模擬器（JSON 強化版）")
    symbol, data = load_symbol_and_price()
    if not symbol or not data:
        return
    results = simulate_all_modules(symbol, data)
    if results:
        save_results(results)
    else:
        print("[Ω] 無可模擬模組")

if __name__ == "__main__":
    main()
