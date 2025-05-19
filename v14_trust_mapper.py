# /mnt/data/hello/v14_trust_mapper.py
import json
import os
from datetime import datetime

TRUST_FILE = "/mnt/data/hello/trust_map.json"
HISTORY_FILE = "/mnt/data/hello/trust_history.json"

def load_trust_map():
    if not os.path.exists(TRUST_FILE):
        print("[Ω] 沒有找到信心圖譜，請先執行 v11")
        return {}
    with open(TRUST_FILE, "r") as f:
        return json.load(f)

def update_trust_history(trust_map):
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    else:
        history = {}

    timestamp = datetime.now().isoformat()

    for mod, info in trust_map.items():
        mod_history = history.get(mod, [])
        mod_history.append({
            "time": timestamp,
            "score": info.get("score", 0),
            "recommended": info.get("recommended", False)
        })
        history[mod] = mod_history

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)
    print(f"[Ω] 已更新 {len(trust_map)} 支模組的信心歷程。")

def main():
    trust_map = load_trust_map()
    update_trust_history(trust_map)

if __name__ == "__main__":
    main()
