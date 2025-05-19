import os
import json
import random
from datetime import datetime

MODULE_DIR = "/mnt/data/hello/modules"
LOG_PATH = "/mnt/data/hello/module_log.json"
PRICE_DIR = "/mnt/data/hello/prices"
SYMBOL_LIST_PATH = "/mnt/data/hello/top_symbols.json"
TOP_N = 3
BUILD_PER_SYMBOL = 5

os.makedirs(MODULE_DIR, exist_ok=True)

def get_risk_parameters():
    import importlib.util
    path = os.path.join(os.path.dirname(__file__), "v05_capital_core.py")
    spec = importlib.util.spec_from_file_location("v05_capital_core", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.get_risk_parameters()

def load_real_data(symbol):
    filepath = os.path.join(PRICE_DIR, f"{symbol}.json")
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as f:
        raw = json.load(f)
        if len(raw) < 20:
            return None
        return {
            "rsi": [c["close"] for c in raw][-14:],
            "macd": [c["close"] for c in raw][-26:],
            "signal": [c["close"] for c in raw][-26:],
            "ma": [c["close"] for c in raw][-10:],
            "close": [c["close"] for c in raw],
            "atr": [c["high"] - c["low"] for c in raw][-14:]
        }

def simulate_module(module_code, data, history):
    local_env = {}
    try:
        exec(module_code, local_env)
        if "run" not in local_env:
            return -999
        result = local_env["run"](data, capital=history["initial_capital"], history=history)
        return result.get("score", -999)
    except Exception as e:
        return -999

def generate_candidate_module():
    try:
        with open("/mnt/data/hello/template_logic.py", "r") as f:
            logic = f.read()
    except:
        return None
    risk = get_risk_parameters()
    code = f"""
def run(data, capital, history):
    log = []
    initial = capital
    max_risk = {risk['max_risk']}
    position_size = {risk['position_size']}
{logic}
    return {{
        "log": log,
        "final_capital": capital,
        "score": capital - initial
    }}
""".strip()
    return code

def log_module(filename, score, tag):
    try:
        log_data = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                log_data = json.load(f)
        log_data.append({
            "module": filename,
            "score": round(score, 4),
            "indicator": tag,
            "created": datetime.now().isoformat()
        })
        with open(LOG_PATH, "w") as f:
            json.dump(log_data, f, indent=2)
    except:
        pass

def main():
    if not os.path.exists(SYMBOL_LIST_PATH):
        print("[×] 找不到 top_symbols.json，請先執行選幣模組")
        return
    with open(SYMBOL_LIST_PATH, "r") as f:
        symbols = json.load(f)

    candidates = []
    for symbol in symbols[:5]:
        data = load_real_data(symbol)
        if not data:
            continue
        history = {"initial_capital": get_risk_parameters()["capital"]}
        for _ in range(BUILD_PER_SYMBOL):
            code = generate_candidate_module()
            if code:
                score = simulate_module(code, data, history)
                print(f"[候選] {symbol} 得分：{score}")
                candidates.append((score, code, symbol))

    if not candidates:
        print("[×] 無模組產生")
        return

    best_models = sorted(candidates, key=lambda x: x[0], reverse=True)[:TOP_N]
    for model in best_models:
        score, code, symbol = model
        filename = f"module_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{symbol}_garou.py"
        with open(os.path.join(MODULE_DIR, filename), "w") as f:
            f.write(code)
        log_module(filename, score, f"{symbol}-garou")
        print(f"[✓] 儲存：{filename}，score={score:.2f}")

if __name__ == "__main__":
    main()
