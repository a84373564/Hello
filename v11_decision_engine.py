import json
import os

SCORE_FILE = "module_scores.json"
TRUST_FILE = "trust_map.json"

# 設定門檻
MIN_SCORE = 5       # 淨利潤需超過 5 USDT
MIN_WIN_RATE = 0.6  # 勝率需超過 60%
MAX_DRAWDOWN = 0.3  # 最大回撤不得超過 30%
MIN_SHARPE = 1.0    # Sharpe ratio 至少為 1.0

def load_scores():
    if not os.path.exists(SCORE_FILE):
        print("[Ω] 找不到模組績效檔案，請先執行 v10")
        return {}
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def update_trust_map(recommendations):
    if not os.path.exists(TRUST_FILE):
        trust_map = {}
    else:
        with open(TRUST_FILE, "r") as f:
            trust_map = json.load(f)

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
    print("[Ω] 信心圖譜已更新。")

def main():
    scores = load_scores()
    recommendations = {}
    for mod, s in scores.items():
        if (
            s["score"] >= MIN_SCORE and
            s["win_rate"] >= MIN_WIN_RATE and
            s["max_drawdown"] <= MAX_DRAWDOWN and
            s["sharpe"] >= MIN_SHARPE
        ):
            recommendations[mod] = "RECOMMENDED"
        else:
            recommendations[mod] = "REJECTED"
        print(f"[Ω] 模組 {mod}: {recommendations[mod]}")

    update_trust_map(recommendations)

if __name__ == "__main__":
    main()
