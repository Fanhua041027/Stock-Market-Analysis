#!/bin/bash
echo "Initializing environment..."

# 检查必要的目录结构
if [ ! -d "/app/code" ]; then
    mkdir -p /app/code
fi

if [ ! -d "/app/data" ]; then
    mkdir -p /app/data
fi

if [ ! -d "/app/model" ]; then
    mkdir -p /app/model
fi

if [ ! -d "/app/output" ]; then
    mkdir -p /app/output
fi

if [ ! -d "/app/temp" ]; then
    mkdir -p /app/temp
fi

echo "Environment initialized successfully!"