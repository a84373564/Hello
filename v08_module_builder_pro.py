import os
import json
import random
from datetime import datetime

MODULE_DIR = "/mnt/data/hello/modules"
TEMP_DIR = "/mnt/data/hello/_temp_modules"
os.makedirs(MODULE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# 動態載入 v05_capital_core
def get_risk_parameters():
    import importlib.util
    path = os.path.join(os.path.dirname(__file__), "v05_capital_core.py")
    spec = importlib.util.spec_from_file_location("v05_capital_core", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.get_risk_parameters()

# 動態載入 indicator_library
def get_indicator_logic(indicator):
    import importlib.util
    path = os.path.join(os.path.dirname(__file__), "indicator_library.py")
    spec = importlib.util.spec_from_file_location("indicator_library", path)
    lib = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lib)
    return lib.get_indicator_logic(indicator)

# 模擬模組執行邏輯
def simulate_module(module_code, data, history):
    local_env = {}
    try:
        exec(module_code, local_env)
        if "run" not in local_env:
            return -999
        result = local_env["run"](data, capital=history["initial_capital"], history=history)
        return result.get("score", -999)
    except Exception:
        return -999

# 假資料（供模擬）
def mock_data():
    return {
        "rsi": [40, 32, 28],
        "macd": [0.002, 0.004, 0.006],
        "signal": [0.003, 0.0035, 0.0032],
        "ma": [100, 102, 105],
        "close": [101, 106, 104],
        "atr": [1.1, 1.2, 1.3]
    }

# 建構候選模組
def generate_candidate_module(indicator):
    logic = get_indicator_logic(indicator)
    if logic is None:
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

# 主流程：模擬 + 精選最強模組
def main():
    indicators = ["rsi", "macd", "ma", "atr"]
    candidates = []
    data = mock_data()
    history = {"initial_capital": get_risk_parameters()["capital"]}

    for _ in range(8):
        ind = random.choice(indicators)
        code = generate_candidate_module(ind)
        if code:
            score = simulate_module(code, data, history)
            candidates.append((score, code, ind))

    if not candidates:
        print("[×] 無可用模組產生")
        return

    best = sorted(candidates, key=lambda x: x[0], reverse=True)[0]
    best_score, best_code, best_ind = best

    filename = f"module_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{best_ind}.py"
    with open(os.path.join(MODULE_DIR, filename), "w") as f:
        f.write(best_code)

    print(f"[✓] 最強模組已產生：{filename}，score={best_score:.2f}")

if __name__ == "__main__":
    main()
