import json
from datetime import datetime

CAPITAL_FILE = "capital_tracker.json"

def load_capital():
    try:
        with open(CAPITAL_FILE, "r") as f:
            data = json.load(f)
            return float(data.get("current_capital", 0))
    except Exception:
        return 0

def update_capital(new_value):
    with open(CAPITAL_FILE, "r") as f:
        data = json.load(f)
    data["current_capital"] = float(new_value)
    data["updated"] = datetime.now().isoformat()
    with open(CAPITAL_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[Ω] 資金更新為 {new_value:.2f} USDT")

def reset_capital():
    with open(CAPITAL_FILE, "r") as f:
        data = json.load(f)
    initial = float(data.get("initial_capital", 100))
    data["current_capital"] = initial
    data["updated"] = datetime.now().isoformat()
    with open(CAPITAL_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print(f"[Ω] 資金重置為初始值 {initial:.2f} USDT")

def get_risk_parameters():
    capital = load_capital()
    return {
        "capital": capital,
        "max_risk": round(capital * 0.03, 2),
        "position_size": round(capital * 0.1, 2),
        "min_capital": 10
    }

if __name__ == "__main__":
    print("[Ω] 當前資金：", load_capital(), "USDT")
    print("[Ω] 風控參數：", get_risk_parameters())
