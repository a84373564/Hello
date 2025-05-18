import os
import json

MODULE_DIR = "modules"
TRUST_FILE = "trust_map.json"
CLEAN_THRESHOLD = -3
MAX_MODULES = 100

def load_trust_map():
    if not os.path.exists(TRUST_FILE):
        print("[Ω] 找不到信心圖譜，請先執行 v11")
        return {}
    with open(TRUST_FILE, "r") as f:
        return json.load(f)

def clean_low_trust_modules(trust_map):
    removed = []
    for mod, trust in list(trust_map.items()):
        if trust.get("score", 0) <= CLEAN_THRESHOLD:
            mod_path = os.path.join(MODULE_DIR, mod)
            if os.path.exists(mod_path):
                os.remove(mod_path)
                removed.append(mod)
                print(f"[Ω] 模組 {mod} 已清除（信心過低）")
                trust_map.pop(mod)
    return removed

def clean_excess_modules(trust_map):
    current_modules = [f for f in os.listdir(MODULE_DIR) if f.endswith(".py")]
    if len(current_modules) <= MAX_MODULES:
        return []

    # 排序：從信心最低的開始刪
    ranked = sorted(trust_map.items(), key=lambda x: x[1].get("score", 0))
    to_remove = len(current_modules) - MAX_MODULES
    removed = []

    for mod, _ in ranked:
        if mod in current_modules:
            mod_path = os.path.join(MODULE_DIR, mod)
            if os.path.exists(mod_path):
                os.remove(mod_path)
                removed.append(mod)
                trust_map.pop(mod)
                print(f"[Ω] 模組 {mod} 已清除（超出模組上限）")
                to_remove -= 1
                if to_remove == 0:
                    break

    return removed

def main():
    trust_map = load_trust_map()
    removed_low = clean_low_trust_modules(trust_map)
    removed_excess = clean_excess_modules(trust_map)

    total_removed = removed_low + removed_excess
    if total_removed:
        with open(TRUST_FILE, "w") as f:
            json.dump(trust_map, f, indent=2)
        print(f"[Ω] 總共清除 {len(total_removed)} 支模組。")
    else:
        print("[Ω] 沒有需要清除的模組。")

if __name__ == "__main__":
    main()
