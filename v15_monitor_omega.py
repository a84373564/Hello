# /mnt/data/hello/v15_monitor_omega.py
import json
import os

SCORE_FILE = "/mnt/data/hello/module_scores.json"
TRUST_FILE = "/mnt/data/hello/trust_map.json"
RECOMMENDED_FILE = "/mnt/data/hello/recommended_modules.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[!] 缺少資料檔案：{path}")
        return {}
    with open(path, "r") as f:
        return json.load(f)

def monitor():
    scores = load_json(SCORE_FILE)
    trust = load_json(TRUST_FILE)
    recommended = load_json(RECOMMENDED_FILE)
    if isinstance(recommended, list):
        recommended_set = set(recommended)
    else:
        recommended_set = set()

    modules = []
    for mod, data in scores.items():
        entry = {
            "name": mod,
            "score": data.get("score", 0),
            "win_rate": data.get("win_rate", 0),
            "profit": data.get("profit", 0),
            "drawdown": data.get("drawdown", 0),
            "sharpe": data.get("sharpe", 0),
            "trust": trust.get(mod, {}).get("score", 0),
            "recommended": mod in recommended_set
        }
        modules.append(entry)

    sorted_mods = sorted(modules, key=lambda x: x["score"], reverse=True)

    print("模組排行榜（依照 score 排名）：\n")
    for idx, m in enumerate(sorted_mods):
        mark = "★" if m["recommended"] else " "
        print(f"{idx+1:>2}. {mark} {m['name']}")
        print(f"    Profit={m['profit']}  Win={m['win_rate']}  Draw={m['drawdown']}  Sharpe={m['sharpe']}  Score={m['score']}  Trust={m['trust']}")
    print("\n[*] 模組總數：", len(sorted_mods))

def main():
    monitor()

if __name__ == "__main__":
    main()
