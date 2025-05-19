# /mnt/data/hello/v12_recommender_omega.py
import os
import json

TRUST_FILE = "/mnt/data/hello/trust_map.json"
OUTPUT_FILE = "/mnt/data/hello/recommended_modules.json"

def load_trust_map():
    if not os.path.exists(TRUST_FILE):
        print("[!] 找不到信心圖譜 trust_map.json，請先執行 v11")
        return {}
    with open(TRUST_FILE, "r") as f:
        return json.load(f)

def select_recommended(trust_map):
    selected = []
    for mod, info in trust_map.items():
        if info.get("recommended") and info.get("score", 0) >= 3:
            selected.append(mod)
            print(f"[◎] 推薦模組：{mod}（score={info.get('score')}）")
    return selected

def save_recommendations(modules):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(modules, f, indent=2)
    print(f"[*] 已寫入推薦模組 {len(modules)} 筆 → {OUTPUT_FILE}")

def main():
    trust_map = load_trust_map()
    if not trust_map:
        return
    recommendations = select_recommended(trust_map)
    save_recommendations(recommendations)

if __name__ == "__main__":
    main()
