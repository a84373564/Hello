import os
import json

MODULE_PATH = "/mnt/data/hello/modules/"
MEMORY_FILE = "/mnt/data/hello/memory_record.json"

def is_valid_module(file_path):
    try:
        with open(file_path, "r") as f:
            source = f.read()
        compile(source, file_path, 'exec')
        return True
    except Exception as e:
        print(f"[X] 語法錯誤模組：{file_path.split('/')[-1]} → {e}")
        return False

def is_failed_module(file_path):
    try:
        with open(file_path, "r") as f:
            code = f.read()
        if "'score':" in code and "'final_capital':" in code:
            score_line = [line for line in code.splitlines() if "'score':" in line]
            capital_line = [line for line in code.splitlines() if "'final_capital':" in line]
            if score_line and capital_line:
                score = float(score_line[0].split(":")[-1].strip().strip(","))
                capital = float(capital_line[0].split(":")[-1].strip().strip(","))
                if score < 0 or capital <= 100:
                    print(f"[X] 績效不佳模組：{file_path.split('/')[-1]} → score={score}, capital={capital}")
                    return True
        return False
    except Exception:
        return True

def remove_module(file_path):
    print(f"[!] 移除模組：{file_path.split('/')[-1]}")
    os.remove(file_path)

def clean_modules():
    files = os.listdir(MODULE_PATH)
    for file in files:
        if not file.endswith(".py"):
            continue
        path = os.path.join(MODULE_PATH, file)
        if not is_valid_module(path) or is_failed_module(path):
            remove_module(path)

def clean_memory():
    if not os.path.exists(MEMORY_FILE):
        return
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
    new_memory = [m for m in memory if os.path.exists(os.path.join(MODULE_PATH, f"{m['name']}.py"))]
    with open(MEMORY_FILE, "w") as f:
        json.dump(new_memory, f, indent=2)
    print(f"[O] 已同步 memory_record.json，有效模組剩下：{len(new_memory)}")

if __name__ == "__main__":
    clean_modules()
    clean_memory()
