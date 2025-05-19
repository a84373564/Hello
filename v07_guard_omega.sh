import os
import time
import subprocess
from datetime import datetime

CYCLE_FILE = "/mnt/data/hello/.cycle_count"
MODULES_DIR = "/mnt/data/hello"
LOGFILE = "/mnt/data/hello/guard.log"
MAX_LOG_SIZE = 1000 * 1024  # 1MB
MAX_LOG_BACKUPS = 5

# 模組分層
HIGH_FREQ = [
    "v03_symbol_screener_omega.py",
    "v04_price_fetcher.py",
    "v05_capital_core.py",
    "v08_module_builder.py",
    "v09_simulator_realistic.py",
    "v10_performance_evaluator.py",
    "v11_decision_engine.py",
    "v12_recommender_omega.py",
    "v13_cleaner_omega.py",
    "v16.5_tactical_pruner.py"
]

MID_FREQ = {
    "v17_elite_saver.py": 3,
    "v18_mutation_mixer.py": 2,
    "v19_strategy_fusioner.py": 2,
    "v20_strategy_generator.py": 5
}

LOW_FREQ = {
    "v21_gene_analyzer.py": 10,
    "v22_performance_tracker.py": 5,
    "v23_system_risk_analyzer.py": 10
}

def rotate_log():
    if os.path.exists(LOGFILE) and os.path.getsize(LOGFILE) > MAX_LOG_SIZE:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"/mnt/data/hello/guard_{timestamp}.log"
        os.rename(LOGFILE, backup_name)
        # 清除多餘備份
        logs = sorted([
            f for f in os.listdir("/mnt/data/hello")
            if f.startswith("guard_") and f.endswith(".log")
        ])
        while len(logs) > MAX_LOG_BACKUPS:
            os.remove(os.path.join("/mnt/data/hello", logs.pop(0)))

def get_cycle():
    if os.path.exists(CYCLE_FILE):
        with open(CYCLE_FILE, "r") as f:
            return int(f.read().strip()) + 1
    return 1

def save_cycle(cycle):
    with open(CYCLE_FILE, "w") as f:
        f.write(str(cycle))

def run_module(filename):
    path = os.path.join(MODULES_DIR, filename)
    if os.path.exists(path):
        with open(LOGFILE, "a") as log:
            log.write(f"[+] 執行模組：{filename}\n")
        subprocess.call(["python3", path])
    else:
        with open(LOGFILE, "a") as log:
            log.write(f"[!] 模組不存在：{filename}\n")

def count_modules():
    mod_path = os.path.join(MODULES_DIR, "modules")
    if os.path.exists(mod_path):
        return len([f for f in os.listdir(mod_path) if f.endswith(".json")])
    return 0

def main():
    while True:
        rotate_log()

        cycle = get_cycle()
        with open(LOGFILE, "a") as log:
            log.write(f"\n--- 第 {cycle} 輪演化開始 ---\n")

        for mod in HIGH_FREQ:
            run_module(mod)

        for mod, freq in MID_FREQ.items():
            if cycle % freq == 0:
                run_module(mod)

        for mod, freq in LOW_FREQ.items():
            if cycle % freq == 0:
                run_module(mod)

        total = count_modules()
        with open(LOGFILE, "a") as log:
            log.write(f"[✓] 第 {cycle} 輪完成，當前模組數：{total}\n")

        save_cycle(cycle)
        time.sleep(60)

if __name__ == "__main__":
    main()
