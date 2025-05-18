import json
import os

SCORES_FILE = "module_scores.json"
TRUST_FILE = "trust_map.json"
RECOMMENDED_FILE = "recommended_modules.json"

def load_json(path):
    if not os.path.exists(path):
        print(f"[Ω] 無法讀取 {path}")
        return {}
    with open(path, "r") as f:
        return json.load(f)

def sharpe_to_stars(sharpe):
    if sharpe >= 2: return "★★★★★"
    elif sharpe >= 1.5: return "★★★★☆"
    elif sharpe >= 1.0: return "★★★☆☆"
    elif sharpe >= 0.5: return "★★☆☆☆"
    elif sharpe > 0: return "★☆☆☆☆"
    else: return "☆☆☆☆☆"

def display_top_modules(scores, trust_map, recommended_list, top_n=10):
    sorted_mods = sorted(scores.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    print("═════════════════ Sovereign AI 策略排行榜 ═════════════════")
    print(f"{'模組名稱':<20}{'淨賺金額':>8}{'勝率':>10}{'穩定度':>10}{'最慘跌幅':>10}{'信心':>8}{'推薦':>6}")
    print("────────────────────────────────────────────────────────")
    for mod, s in sorted_mods[:top_n]:
        score = s.get('score', 0)
        win_rate = f"{s.get('win_rate', 0) * 100:.1f}%"
        drawdown = f"-{s.get('max_drawdown', 0) * 100:.1f}%"
        stars = sharpe_to_stars(s.get('sharpe', 0))
        trust = trust_map.get(mod, {}).get("score", 0)
        trust_label = f"+{trust}" if trust > 0 else str(trust)
        tag = "✓" if mod in recommended_list else "-"
        profit_str = f"+{score:.2f}" if score >= 0 else f"{score:.2f}"
        print(f"{mod:<20}{profit_str:>8}{win_rate:>10}{stars:>10}{drawdown:>10}{trust_label:>8}{tag:>6}")
    print("════════════════════════════════════════════════════════")

def main():
    scores = load_json(SCORES_FILE)
    trust_map = load_json(TRUST_FILE)
    recommended = load_json(RECOMMENDED_FILE) if os.path.exists(RECOMMENDED_FILE) else []

    if not scores:
        print("[Ω] 尚未有模組績效資料。請先執行 v09～v10。")
        return

    display_top_modules(scores, trust_map, recommended)

if __name__ == "__main__":
    main()
