#!/bin/bash

echo "Training model..."

# 固定随机种子
export PYTHONHASHSEED=42

# 运行训练脚本
python code/train.py

echo "Model trained successfully!"