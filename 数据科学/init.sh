#!/bin/bash

echo "Initializing environment..."

# 检查必要的目录结构
if [ ! -d "/app/code" ]; then
    mkdir -p /app/code
fi

if [ ! -d "/app/data" ]; then
    mkdir -p /app/data
fi

echo "Environment initialized successfully!"