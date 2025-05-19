import os
import json
import random
from indicator_library import get_indicator_logic
from v05_capital_core import get_risk_parameters

MODULE_DIR = "/mnt/data/hello/modules"
MEMORY_PATH = "/mnt/data/hello/memory/trust_map.json"
TOP_SYMBOLS_PATH = "/mnt/data/hello/top_symbols.json"

os.makedirs(MODULE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

def generate_module(symbol):
    indicator = random.choice(["rsi", "macd", "ma", "atr"])
    logic = get_indicator_logic(indicator)
    if logic is None:
        print(f"[跳過] 不支援的指標：{indicator}")
        return None

    risk_params = get_risk_parameters()
    capital = risk_params["capital"]
    max_risk = risk_params["max_risk"]
    position_size = risk_params["position_size"]

    code = f"""
def run(data, capital, history):
    log = []
    capital = {capital}  # 起始資金
    max_risk = {max_risk}  # 最大風險承擔
    position_size = {position_size}  # 單次下單金額
{logic}
    return {{
        'log': log,
        'final_capital': capital,
        'score': capital - history.get('initial_capital', 100)
    }}
""".strip()

    return code

def update_memory(filename, indicator):
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            memory = json.load(f)
    else:
        memory = {}
    memory[filename] = {"indicator": indicator}
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)
