import os
import subprocess

CYCLE_FILE = "/mnt/data/hello/.cycle_count"
MODULES_DIR = "/mnt/data/hello"
CYCLE = 1

# 高頻模組：每輪都跑
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

# 中頻模組：每 N 輪執行一次
MID_FREQ = {
    "v17_elite_saver.py": 3,
    "v18_mutation_mixer.py": 2,
    "v19_strategy_fusioner.py": 2,
    "v20_strategy_generator.py": 5
}

# 低頻模組：偶爾執行的分析與優化
LOW_FREQ = {
    "v21_gene_analyzer.py": 10,
    "v22_performance_tracker.py": 5,
    "v23_system_risk_analyzer.py": 10
}

def run_module(filename):
    path = os.path.join(MODULES_DIR, filename)
    if os.path.exists(path):
        print(f"[+] 執行模組：{filename}")
        subprocess.call(["python3", path])
    else:
        print(f"[!] 模組不存在：{filename}")

def get_cycle():
    if os.path.exists(CYCLE_FILE):
        with open(CYCLE_FILE, "r") as f:
            return int(f.read().strip()) + 1
    return 1

def save_cycle(cycle):
    with open(CYCLE_FILE, "w") as f:
        f.write(str(cycle))

def main():
    global CYCLE
    CYCLE = get_cycle()
    print(f"--- 執行週期：第 {CYCLE} 輪 ---")

    for mod in HIGH_FREQ:
        run_module(mod)

    for mod, freq in MID_FREQ.items():
        if CYCLE % freq == 0:
            run_module(mod)

    for mod, freq in LOW_FREQ.items():
        if CYCLE % freq == 0:
            run_module(mod)

    save_cycle(CYCLE)
    print(f"[✓] 執行完成，第 {CYCLE} 輪已記錄")

if __name__ == "__main__":
    main()
