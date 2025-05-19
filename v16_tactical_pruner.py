import os
import json

LOG_PATH = "module_log.json"
MODULE_DIR = "modules"
MAX_MODULES = 100  # 只保留前 100 名

print("[v16] 啟動精英模組修剪器")

if not os.path.exists(LOG_PATH):
    print("[!] 尚無模組績效記錄，略過修剪")
    exit(0)

with open(LOG_PATH) as f:
    logs = json.load(f)

# 依 score 排序，取前 100 名模組
logs_sorted = sorted(logs, key=lambda x: x.get("score", 0), reverse=True)
elite_files = set([entry.get("file") for entry in logs_sorted[:MAX_MODULES]])

# 刪除模組資料夾中其餘不是精英的
removed = 0
for fname in os.listdir(MODULE_DIR):
    if not fname.endswith(".py"):
        continue
    if fname not in elite_files:
        path = os.path.join(MODULE_DIR, fname)
        try:
            os.remove(path)
            removed += 1
            print(f"[v16] 移除非精英模組：{fname}")
        except Exception as e:
            print(f"[!] 無法刪除 {fname}，錯誤：{e}")

print(f"[v16] 精英修剪完成，已保留 {MAX_MODULES} 支模組，剃除 {removed} 支")
