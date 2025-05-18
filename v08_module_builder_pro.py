import os
import json
import random
from indicator_library import get_indicator_logic

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

    code = f"""
def run(data, capital, history):
{logic}
    return {{
        'log': log,
        'final_capital': capital,
        'score': capital - history.get('initial_capital', 100)
    }}
"""
    return code.strip()

def update_memory(filename, indicator):
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "r") as f:
            memory = json.load(f)
    else:
        memory = {}
    memory[filename] = {"indicator": indicator}
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def main():
    with open(TOP_SYMBOLS_PATH, "r") as f:
        symbols = json.load(f)

    for symbol in symbols:
        filename = f"mod_{symbol.lower()}_{random.randint(1000,9999)}.py"
        path = os.path.join(MODULE_DIR, filename)
        code = generate_module(symbol)
        if code:
            with open(path, "w") as f:
                f.write(code)
            update_memory(filename, "auto")

if __name__ == "__main__":
    main()
