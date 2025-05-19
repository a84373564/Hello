import os
import json
from datetime import datetime

MODULE_DIR = "/mnt/data/hello/modules"
LOG_PATH = "/mnt/data/hello/module_log.json"
THRESHOLD = 0.0  # 分數低於此值的模組會被刪除

def load_log():
    if not os.path.exists(LOG_PATH):
        print("[×] 無 module_log.json，無法進行清理")
        return []
    with open(LOG_PATH, "r") as f:
        return json.load(f)

def delete_module(filename):
    path = os.path.join(MODULE_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        print(f"[−] 已刪除：{filename}")
    else:
        print(f"[!] 模組不存在：{filename}")

def main():
    log = load_log()
    if not log:
        return

    total = 0
    deleted = 0

    for entry in log:
        total += 1
        score = entry.get("score", 0)
        module = entry.get("module")
        if score < THRESHOLD:
            delete_module(module)
            deleted += 1

    print(f"[✓] 清理完成，總模組數：{total}，已刪除：{deleted}")

if __name__ == "__main__":
    main()
