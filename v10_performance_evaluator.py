# /mnt/data/hello/v10_performance_evaluator.py
import os
import json

RECORD_FILE = "/mnt/data/hello/module_records.json"
OUTPUT_FILE = "/mnt/data/hello/module_scores.json"

def evaluate_module(record):
    win_rate = record.get("win_rate", 0)
    drawdown = record.get("drawdown", 0)
    profit = record.get("profit", 0)
    sharpe = round((win_rate * profit) / (drawdown + 1e-6), 4)  # 避免除以 0
    score = round((win_rate * 0.5 + profit * 0.4 - drawdown * 0.1) * sharpe, 4)
    return {
        "symbol": record.get("symbol", "NA"),
        "win_rate": win_rate,
        "profit": profit,
        "drawdown": drawdown,
        "sharpe": sharpe,
        "score": score,
        "source": record.get("module")
    }

def main():
    if not os.path.exists(RECORD_FILE):
        print("[!] 找不到模擬紀錄 module_records.json，請先執行 v09")
        return

    with open(RECORD_FILE, "r") as f:
        records = json.load(f)

    results = {}
    for module, record in records.items():
        results[module] = evaluate_module(record)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"[*] 已計算 {len(results)} 筆模組評分 → 寫入 module_scores.json")

if __name__ == "__main__":
    main()
