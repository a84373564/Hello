import os
import json
from datetime import datetime

print("[Ω] Starting Sovereign Omega2 System...")

os.makedirs("modules", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("strategies", exist_ok=True)

# 檢查是否已有資金紀錄
if not os.path.exists("capital_tracker.json"):
    capital = float(input("請輸入你的起始資金（例如 70.51）: "))
    with open("capital_tracker.json", "w") as f:
        json.dump({
            "initial_capital": capital,
            "current_capital": capital,
            "updated": datetime.now().isoformat()
        }, f, indent=4)
        print(f"[Ω] 初始化資金完成：{capital} USDT")
else:
    with open("capital_tracker.json", "r") as f:
        cap = json.load(f)
        print(f"[Ω] 資金紀錄已存在：目前為 {cap['current_capital']} USDT")

# 模組績效紀錄檔
if not os.path.exists("module_records.json"):
    with open("module_records.json", "w") as f:
        json.dump({}, f)
        print("[Ω] 初始化 module_records.json 完成")

# 信心圖譜初始化
if not os.path.exists("trust_map.json"):
    with open("trust_map.json", "w") as f:
        json.dump({}, f)
        print("[Ω] 初始化 trust_map.json 完成")

print("[Ω] 系統架構準備完成，已可啟動進化流程。")
