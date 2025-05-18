import subprocess

modules = [
    "v08_module_builder.py",
    "v09_simulator_realistic.py",
    "v10_performance_evaluator.py",
    "v11_decision_engine.py",
    "v12_recommender_omega.py",
    "v13_cleaner_omega.py"
]

print("[Ω] Sovereign UltraCore Ω² - 主控啟動")

for mod in modules:
    print(f"[Ω] 執行：{mod}")
    try:
        result = subprocess.run(["python3", mod], check=True)
    except subprocess.CalledProcessError:
        print(f"[Ω] 模組 {mod} 執行失敗，跳過。")

print("[Ω] 本輪演化結束。下一輪請重新啟動主控或由掛機腳本自動執行。")
