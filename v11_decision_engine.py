# /mnt/data/hello/v11_decision_engine.py
import json
import os

SCORE_FILE = "/mnt/data/hello/module_scores.json"
TRUST_FILE = "/mnt/data/hello/trust_map.json"

# 門檻參數（與原版一致）
MIN_SCORE = 5
MIN_WIN_RATE = 0.6
MAX_DRAWDOWN = 0.3
MIN_SHARPE = 1.0

def load_scores():
    if not os.path.exists(SCORE_FILE):
        print("[Ω] 找不到模組績效檔案，請先執行 v10")
        return {}
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def update_trust_map(recommendations):
    if os.path.exists(TRUST_FILE):
        with open(TRUST_FILE, "r") as f:
            trust_map = json.load(f)
    else:
        trust_map = {}

    for mod, status in recommendations.items():
        trust = trust_map.get(mod, {"score": 0, "recommended": False})
        if status == "RECOMMENDED":
            trust["score"] += 1
            trust["recommended"] = True
        elif status == "REJECTED":
            trust["score"] -= 1
            trust["recommended"] = False
        trust_map[mod] = trust

    with open(TRUST_FILE, "w") as f:
        json.dump(trust_map, f, indent=2)
    print("[Ω] 信心圖譜已更新")

def main():
    scores = load_scores()
    recommendations = {}
    for mod, s in scores.items():
        try:
            if (
                s["profit"] >= MIN_SCORE and
                s["win_rate"] >= MIN_WIN_RATE and
                s["drawdown"] <= MAX_DRAWDOWN and
                s["sharpe"] >= MIN_SHARPE
            ):
                recommendations[mod] = "RECOMMENDED"
                print(f"[+] 推薦模組：{mod}")
            else:
                recommendations[mod] = "REJECTED"
                print(f"[x] 拒絕模組：{mod}")
        except Exception as e:
            print(f"[!] 模組分析失敗 {mod}：{e}")

    update_trust_map(recommendations)

if __name__ == "__main__":
    main()
