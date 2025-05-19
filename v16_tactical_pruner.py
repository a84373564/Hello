# /mnt/data/hello/v16_tactical_pruner.py
import os
import json

MODULE_DIR = "/mnt/data/hello/modules"
SCORE_FILE = "/mnt/data/hello/module_scores.json"
MAX_MODULES = 100

def load_scores():
    if not os.path.exists(SCORE_FILE):
        print("[!] 找不到 module_scores.json，請先執行 v10")
        return {}
    with open(SCORE_FILE, "r") as f:
        return json.load(f)

def prune_top_modules(scores):
    # 對照你原始邏輯：取前 N 名模組檔案名
    sorted_entries = sorted(scores.items(), key=lambda x: x[1].get("score", 0), reverse=True)
    keep_set = set(entry[0] for entry in sorted_entries[:MAX_MODULES])

    removed = 0
    for fname in os.listdir(MODULE_DIR):
        if not fname.endswith(".json"):
            continue
        if fname not in keep_set:
            os.remove(os.path.join(MODULE_DIR, fname))
            removed += 1
            print(f"[×] 剃除模組：{fname}")

    print(f"[✓] 修剪完成，只保留前 {MAX_MODULES}，共剃除 {removed} 支模組")

def main():
    scores = load_scores()
    prune_top_modules(scores)

if __name__ == "__main__":
    main()
