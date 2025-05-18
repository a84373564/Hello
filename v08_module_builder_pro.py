import random
import os
import string

TEMPLATE = """
def run(data, capital, history):
    log = []
    position = None
    entry_price = 0
    for i, candle in enumerate(data):
        if position is None and {buy_condition}:
            position = 'LONG'
            entry_price = candle['close']
            log.append({{"action": "buy", "price": entry_price, "index": i}})
        elif position == 'LONG' and {sell_condition}:
            exit_price = candle['close']
            profit = (exit_price - entry_price) / entry_price
            capital += capital * profit
            log.append({{"action": "sell", "price": exit_price, "index": i, "profit": profit}})
            position = None
    return {{
        "log": log,
        "final_capital": capital,
        "score": capital - history.get("initial_capital", 100)
    }}
"""

BUY_OPTIONS = [
    "candle['rsi'] < 30",
    "candle['macd'] > candle['macdsignal']",
    "candle['k'] < candle['d']",
    "candle['close'] < candle['bb_lower']",
    "candle['ma5'] > candle['ma20']",
    "candle['atr'] > candle['atr_avg']",
    "candle['obv'] > candle['obv_ma']"
]

SELL_OPTIONS = [
    "candle['rsi'] > 70",
    "candle['macd'] < candle['macdsignal']",
    "candle['k'] > 80",
    "candle['close'] > candle['bb_upper']",
    "candle['ma5'] < candle['ma20']",
    "candle['atr'] < candle['atr_avg']",
    "candle['obv'] < candle['obv_ma']"
]

def generate_module():
    buy = " and ".join(random.sample(BUY_OPTIONS, k=random.randint(2, 3)))
    sell = " or ".join(random.sample(SELL_OPTIONS, k=random.randint(2, 3)))
    code = TEMPLATE.format(buy_condition=buy, sell_condition=sell)
    return code

def save_module(code):
    os.makedirs("modules", exist_ok=True)
    name = "mod_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + ".py"
    with open(f"modules/{name}", "w") as f:
        f.write(code)
    print(f"[Î©] å¼·åæ¨¡çµå·²ç¢çï¼{name}")

if __name__ == "__main__":
    count = random.randint(2, 3)
    for _ in range(count):
        code = generate_module()
        save_module(code)
