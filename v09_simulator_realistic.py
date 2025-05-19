import os
import json
import importlib.util

MODULE_DIR = "modules"
PRICE_DIR = "prices"
RESULT_FILE = "sim_result.json"

def load_data(symbol):
    try:
        with open(f"{PRICE_DIR}/{symbol}.json") as f:
            raw = json.load(f)
            return {"close": raw["close"]}
    except Exception as e:
        print(f"[!] 載入資料失敗 {symbol}：{e}")
        return None

def simulate_module(module_file):
    try:
        name = os.path.splitext(module_file)[0]
        spec = importlib.util.spec_from_file_location(name, os.path.join(MODULE_DIR, module_file))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        if not hasattr(mod, "run"):
            print(f"[!] {module_file} 缺少 run()")
            return None

        symbol = module_file.split("_")[-2]
        data = load_data(symbol)
        if not data:
            return None

        result = mod.run(data, capital=70, history={})
        return result

    except Exception as e:
        print(f"[!] 模組 {module_file} 模擬錯誤：{e}")
        return None

if __name__ == "__main__":
    modules = [f for f in os.listdir(MODULE_DIR) if f.endswith(".py")]
    results = []

    for m in modules:
        res = simulate_module(m)
        if res:
            results.append(res)

    with open(RESULT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[✓] 模擬完成：共 {len(results)} 支模組")
