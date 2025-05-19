import os
import json
from datetime import datetime
import importlib.util

MODULE_DIR = "modules"
PRICE_DIR = "prices"
SYMBOL_LIST = "top_symbols.json"
LOG_PATH = "module_log.json"
TEMPLATE_LOGIC = "template_logic.py"
BUILD_PER_SYMBOL = 5
MAX_SYMBOLS = 3

os.makedirs(MODULE_DIR, exist_ok=True)

def get_risk_parameters():
    try:
        spec = importlib.util.spec_from_file_location("v05", "v05_capital_core.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.get_risk_parameters()
    except:
        return {
            "capital": 70,
            "max_risk": 3.5,
            "position_size": 7,
            "min_capital": 10
        }

def load_real_data(symbol):
    try:
        with open(os.path.join(PRICE_DIR, f"{symbol}.json"), "r") as f:
            raw = json.load(f)
        return {"close": [c["close"] for c in raw]}
    except:
        return None

def simulate_module(code, data, history):
    local_env = {}
    try:
        exec(code, local_env)
        if "run" not in local_env:
            return -999
        result = local_env["run"](data, capital=history["initial_capital"], history=history)
        return result.get("score", -999)
    except Exception as e:
        print("[×] 模組模擬錯誤：", e)
        return -999

def generate_module_code(risk):
    try:
        with open(TEMPLATE_LOGIC, "r") as f:
            logic = f.read()
        indented = "\n".join(["    " + line for line in logic.splitlines()])
        code = f'''
def run(data, capital, history):
    log = []
    initial = capital
    max_risk = {risk["max_risk"]}
    position_size = {risk["position_size"]}
    min_capital = {risk["min_capital"]}
{indented}
    return {{
        "log": log,
        "final_capital": capital,
        "score": capital - initial
    }}
'''.strip()
        return code
    except Exception as e:
        print("[×] 模組產生錯誤：", e)
        return None

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
    if not os.path.exists(SYMBOL_LIST):
        print("[×] 沒找到 top_symbols.json")
        return
    with open(SYMBOL_LIST, "r") as f:
        symbols = json.load(f)

    risk = get_risk_parameters()
    total_created = 0

    for symbol in symbols[:MAX_SYMBOLS]:
        data = load_real_data(symbol)
        if not data:
            continue
        for _ in range(BUILD_PER_SYMBOL):
            code = generate_module_code(risk)
            if code:
                score = simulate_module(code, data, {"initial_capital": risk["capital"]})
                filename = f"module_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{symbol}_mad.py"
                with open(os.path.join(MODULE_DIR, filename), "w") as f:
                    f.write(code)
                log_module(filename, score, f"{symbol}-mad")
                print(f"[✓] 模組儲存：{filename}（score={score:.4f}）")
                total_created += 1

    print(f"[Ω] 本輪總共產出 {total_created} 支模組")

if __name__ == "__main__":
    main()
