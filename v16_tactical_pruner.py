import os
import json

LOG_PATH = "module_log.json"
MODULE_DIR = "modules"
MAX_MODULES = 100  # 最多保留 100 個模組

print("[v16] 啟動策略性修剪器")

if not os.path.exists(LOG_PATH):
    print("[!] 尚無模組績效記錄，略過修剪")
    exit(0)

with open(LOG_PATH) as f:
    logs = json.load(f)

# 只保留有 score 且有 file 欄位的模組，並依 score 由高至低排序
logs_filtered = [entry for entry in logs if "score" in entry and "file" in entry]
logs_sorted = sorted(logs_filtered, key=lambda x: x["score"], reverse=True)
keep_files = set(entry["file"] for entry in logs_sorted[:MAX_MODULES])

removed = 0
for fname in os.listdir(MODULE_DIR):
    if not fname.endswith(".py"):
        continue
    if fname not in keep_files:
        fpath = os.path.join(MODULE_DIR, fname)
        os.remove(fpath)
        removed += 1
        print(f"[x] 剃除模組：{fname}")

print(f"[v16] 修剪完成，僅保留 top {MAX_MODULES}，共剃除 {removed} 支模組")
