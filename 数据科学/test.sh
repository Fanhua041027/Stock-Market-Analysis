#!/bin/bash

echo "Testing model..."

# 固定随机种子
export PYTHONHASHSEED=42

# 运行测试脚本
python code/test.py

echo "Test completed successfully!"
echo "result.csv generated!"