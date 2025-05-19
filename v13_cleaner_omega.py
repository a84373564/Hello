import os

MODULE_DIR = "/mnt/data/hello/modules"

def check_module(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()
        compile(source, file_path, 'exec')
    except Exception as e:
        print(f"[×] 語法錯誤 {file_path}：{e}")

def scan_modules():
    for filename in os.listdir(MODULE_DIR):
        if filename.endswith(".py"):
            full_path = os.path.join(MODULE_DIR, filename)
            check_module(full_path)
            # 額外靜態檢查
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    code = f.read()
                    if '"score":' in code and '"final_capital":' in code:
                        if '"score": 0' in code or '"score": -' in code:
                            print(f"[!] 模組可疑（低分）→ {filename}")
            except Exception as e:
                print(f"[×] 模組讀取錯誤 {filename}：{e}")

if __name__ == "__main__":
    scan_modules()
