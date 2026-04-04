#!/bin/bash
echo "Starting Prediction..."

# 固定随机种子环境变量 (为了可复现性)
export PYTHONHASHSEED=0

python /app/code/test.py

echo "Prediction Done. Check /app/output/result.csv"