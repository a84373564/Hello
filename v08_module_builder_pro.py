import os
import json
import random
import time
from datetime import datetime
from indicator_library import get_indicator_logic
from v05_capital_core import get_risk_parameters

MODULE_DIR = "/mnt/data/hello/modules"
TEMP_DIR = "/mnt/data/hello/_temp_modules"
os.makedirs(MODULE_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# 模擬器（模擬 run() 結果）
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

# 偽造測試資料
def mock_data():
    return {
        "rsi": [40, 32, 28],
        "macd": [0.002, 0.004, 0.006],
        "signal": [0.003, 0.0035, 0.0032],
        "ma": [100, 102, 105],
        "close": [101, 106, 104],
        "atr": [1.1, 1.2, 1.3]
    }

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

def main():
    candidates = []
    indicators = ["rsi", "macd", "ma", "atr"]
    data = mock_data()
    history = {"initial_capital": get_risk_parameters()["capital"]}

    # 生成 8 個模組候選
    for _ in range(8):
        ind = random.choice(indicators)
        code = generate_candidate_module(ind)
        if code:
            score = simulate_module(code, data, history)
            candidates.append((score, code, ind))

    if not candidates:
        print("[×] 無可用模組產生")
        return

    # 選出最高分
    best = sorted(candidates, key=lambda x: x[0], reverse=True)[0]
    best_score, best_code, best_ind = best

    # 寫入模組
    filename = f"module_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{best_ind}.py"
    with open(os.path.join(MODULE_DIR, filename), "w") as f:
        f.write(best_code)

    print(f"[✓] 最強模組已產生：{filename}，score={best_score:.2f}")

if __name__ == "__main__":
    main()
