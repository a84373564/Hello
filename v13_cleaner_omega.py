# /mnt/data/hello/v13_cleaner_omega.py
import os
import json

# 模組路徑與推薦清單來源
MODULE_DIR = "/mnt/data/hello/modules"
RECOMMENDED_FILE = "/mnt/data/hello/recommended_modules.json"

def load_recommended():
    if not os.path.exists(RECOMMENDED_FILE):
        print("[!] 找不到推薦名單 recommended_modules.json，請先執行 v12")
        return []
    with open(RECOMMENDED_FILE, "r") as f:
        return json.load(f)

def clean_modules(keep_list):
    removed = 0
    kept = 0
    for fname in os.listdir(MODULE_DIR):
        if not fname.endswith(".json"):
            continue
        full_path = os.path.join(MODULE_DIR, fname)
        if fname not in keep_list:
            os.remove(full_path)
            removed += 1
            print(f"[×] 已刪除未推薦模組：{fname}")
        else:
            kept += 1
            print(f"[◎] 保留推薦模組：{fname}")
    print(f"[*] 清理完成：保留 {kept}，刪除 {removed}")

def main():
    keep_list = load_recommended()
    if not keep_list:
        print("[!] 推薦名單為空，未進行任何刪除")
        return
    clean_modules(keep_list)

if __name__ == "__main__":
    main()
