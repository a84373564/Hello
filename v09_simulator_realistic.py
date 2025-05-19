import os
import json

def fix_json_prices(folder="prices"):
    for fname in os.listdir(folder):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(folder, fname)
        try:
            with open(path, "r") as f:
                data = json.load(f)
            if isinstance(data, list):
                # 舊格式為 list，轉成 {"close": [...]}
                fixed = {"close": data}
                with open(path, "w") as f:
                    json.dump(fixed, f)
            elif isinstance(data, dict) and "close" not in data:
                # dict 但沒有 close，加上空陣列
                data["close"] = []
                with open(path, "w") as f:
                    json.dump(data, f)
        except Exception as e:
            print(f"[×] 修復 {fname} 失敗：{e}")

import os
import json
import random

MODULE_DIR = "modules"
PRICE_DIR = "prices"
RECORD_FILE = "module_records.json"
SYMBOL_FILE = "top_symbols.json"

def load_price_data():
    if not os.path.exists(SYMBOL_FILE):
        print("[Ω] 找不到 top_symbols.json，請先跑 v03")
        return None, None
    with open(SYMBOL_FILE, "r") as f:
        symbols = json.load(f)
    symbol = random.choice(symbols)
    path = os.path.join(PRICE_DIR, f"price_{symbol}.json")
    if not os.path.exists(path):
        print(f"[Ω] 價格資料不存在：{path}")
        return None, None
    with open(path, "r") as f:
        data = json.load(f)
    return symbol, data

def simulate_module(module_file, symbol, data):
    try:
        local_vars = {}
        with open(os.path.join(MODULE_DIR, module_file)) as f:
            code = f.read()
            exec(code, {}, local_vars)
        mod_run = local_vars["run"]
        result = mod_run(data, 100, {"initial_capital": 100})
        return result
    except Exception as e:
        print(f"[Ω] 模組 {module_file} 模擬錯誤：{e}")
        return None

def save_result(module, result):
    if not os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, "w") as f:
            json.dump({}, f)
    with open(RECORD_FILE, "r") as f:
        records = json.load(f)
    records[module] = result
    with open(RECORD_FILE, "w") as f:
        json.dump(records, f, indent=2)
    print(f"[Ω] 模組 {module} 模擬完成，分數：{result['score']:.2f}")

def main():
    symbol, data = load_price_data()
    if not data:
        return
    for module_file in os.listdir(MODULE_DIR):
        if module_file.endswith(".py"):
            result = simulate_module(module_file, symbol, data)
            if result:
                save_result(module_file, result)

if __name__ == "__main__":
    main()
