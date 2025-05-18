#!/bin/bash

echo "[Ω] 開始自動掛機進化，每輪間隔 180 秒..."
while true; do
    echo "========== $(date) =========="
    python3 v06_ultracore_omega.py
    echo "[Ω] 等待 3 分鐘進入下一輪..."
    sleep 180
done
