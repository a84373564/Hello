import json
import os
import math

RECORD_FILE = "module_records.json"
OUTPUT_FILE = "module_scores.json"

def calculate_performance(log, initial_capital):
    trades = [entry for entry in log if entry["action"] == "sell"]
    if not trades:
        return 0, 0, 0, 0

    wins = [t for t in trades if t["profit"] > 0]
    win_rate = len(wins) / len(trades)

    equity_curve = [initial_capital]
    capital = initial_capital
    for trade in trades:
        capital += capital * trade["profit"]
        equity_curve.append(capital)

    drawdowns = []
    peak = equity_curve[0]
    for cap in equity_curve:
        if cap > peak:
            peak = cap
        dd = (peak - cap) / peak
        drawdowns.append(dd)
    max_drawdown = max(drawdowns)

    returns = [trade["profit"] for trade in trades]
    avg_return = sum(returns) / len(returns)
    stddev = math.sqrt(sum((r - avg_return)**2 for r in returns) / len(returns)) if len(returns) > 1 else 0
    sharpe = avg_return / stddev if stddev > 0 else 0

    return round(win_rate, 4), round(max_drawdown, 4), round(sharpe, 4), round(equity_curve[-1] - initial_capital, 2)

def main():
    if not os.path.exists(RECORD_FILE):
        print("[Î©] å°æªç¼ç¾æ¨¡æ¬ç´éï¼è«åå·è¡ v09")
        return

    with open(RECORD_FILE, "r") as f:
        records = json.load(f)

    scores = {}
    for mod, result in records.items():
        log = result.get("log", [])
        capital = result.get("final_capital", 100)
        initial = result.get("score", 0) + 100
        win_rate, max_dd, sharpe, net_profit = calculate_performance(log, initial)
        scores[mod] = {
            "score": net_profit,
            "win_rate": win_rate,
            "max_drawdown": max_dd,
            "sharpe": sharpe
        }
        print(f"[Î©] {mod} â Score: {net_profit:.2f}, Win: {win_rate:.2%}, DD: {max_dd:.2%}, Sharpe: {sharpe:.2f}")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(scores, f, indent=2)

if __name__ == "__main__":
    main()
