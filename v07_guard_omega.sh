#!/bin/bash

echo "[Ω] 開始自動掛機進化，每輪間隔 180 秒..."

while true; do
    echo "========== $(date) =========="

    python3 v08_module_builder_pro.py
    python3 v09_simulator_realistic.py
    python3 v10_performance_evaluator.py
    python3 v11_decision_engine.py
    python3 v12_recommender_omega.py
    python3 v13_cleaner_omega.py
    python3 v14_trust_mapper.py
    python3 v15_monitor_omega.py
    python3 v16_tactical_pruner.py

    echo "[Ω] 等待 3 分鐘進入下一輪..."
    sleep 180
done
