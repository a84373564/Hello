import json
import os

TRUST_FILE = "trust_map.json"
RECOMMENDED_FILE = "recommended_modules.json"

TRUST_SCORE_THRESHOLD = 3

def load_trust_map():
    if not os.path.exists(TRUST_FILE):
        print("[Ω] 沒有信心圖譜，請先執行 v11")
        return {}
    with open(TRUST_FILE, "r") as f:
        return json.load(f)

def main():
    trust_map = load_trust_map()
    recommended = []

    for mod, record in trust_map.items():
        if record.get("score", 0) >= TRUST_SCORE_THRESHOLD and record.get("recommended", False):
            recommended.append(mod)

    with open(RECOMMENDED_FILE, "w") as f:
        json.dump(recommended, f, indent=2)

    print(f"[Ω] 推薦模組總數：{len(recommended)}")
    for mod in recommended:
        print(f"  → {mod} 已列入推薦池")

if __name__ == "__main__":
    main()
