import os
import json
import random
from datetime import datetime

MODULE_DIR = "/mnt/data/hello/modules"
LOG_PATH = "/mnt/data/hello/module_log.json"
os.makedirs(MODULE_DIR, exist_ok=True)

# 動態載入 v05_capital_core.py
def get_risk_parameters():
    import importlib.util
    path = os.path.join(os.path.dirname(__file__), "v05_capital_core.py")
    spec = importlib.util.spec_from_file_location("v05_capital_core", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.get_risk_parameters()

# 動態載入 indicator_library.py
def get_indicator_logic(indicator):
    import importlib.util
    path = os.path.join(os.path.dirname(__file__), "indicator_library.py")
    spec = importlib.util.spec_from_file_location("indicator_library", path)
    lib = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lib)
    return lib.get_indicator_logic(indicator)

# 模擬模組執行，取得 score
def simulate_module(module_code, data, history):
    local_env = {}
    try:
        exec(module_code, local_env)
        if "run" not in local_env:
            print("[×] 模組未定義 run()")
            return -999
        result = local_env["run"](data, capital=history["initial_capital"], history=history)
        return result.get("score", -999)
    except Exception as e:
        print(f"[×] 模擬錯誤：{str(e)}")
        return -999

# 假資料，會觸發策略邏輯
def mock_data():
    return {
        "rsi": [85, 90, 92],
        "macd": [0.002, 0.004, 0.006],
        "signal": [0.001, 0.002, 0.003],
        "ma": [100, 99, 98],
        "close": [101, 98, 96],
        "atr": [1.1, 1.2, 1.4]
    }

# 建構模組邏輯程式碼
def generate_candidate_module(indicator):
    logic = get_indicator_logic(indicator)
    if logic is None:
        print(f"[×] 不支援指標：{indicator}")
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

# 記錄模組資訊到 module_log.json
def log_module(filename, score, indicator):
    try:
        log_data = []
        if os.path.exists(LOG_PATH):
            with open(LOG_PATH, "r") as f:
                log_data = json.load(f)
        log_data.append({
            "module": filename,
            "score": round(score, 4),
            "indicator": indicator,
            "created": datetime.now().isoformat()
        })
        with open(LOG_PATH, "w") as f:
            json.dump(log_data, f, indent=2)
        print(f"[log] 已記錄：{filename}, score={score}")
    except Exception as e:
        print(f"[×] 紀錄失敗：{str(e)}")

# 主流程
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
            print(f"[候選] {ind} score={score}")
            candidates.append((score, code, ind))

    if not candidates:
        print("[×] 無可用模組產生")
        return

    best = sorted(candidates, key=lambda x: x[0], reverse=True)[0]
    best_score, best_code, best_ind = best

    filename = f"module_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{best_ind}.py"
    with open(os.path.join(MODULE_DIR, filename), "w") as f:
        f.write(best_code)

    log_module(filename, best_score, best_ind)

    print(f"[✓] 最強模組已產生：{filename}，score={best_score:.2f}")

if __name__ == "__main__":
    main()
