#!/bin/bash
echo "Starting Training..."

# 固定随机种子环境变量 (为了可复现性)
export PYTHONHASHSEED=0

python /app/code/train.py

echo "Training Done. Model saved to /app/model/"