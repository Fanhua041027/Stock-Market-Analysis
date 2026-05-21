# Stock Market Analysis —— 股票市场分析

[![Python](https://img.shields.io/badge/Python-3.8+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Python-based stock market analysis tool for data collection, technical analysis, and visualization.

## 功能特性

- **数据获取** — 从公开 API 获取股票历史交易数据
- **技术指标** — 计算移动平均线、RSI、MACD 等常用技术指标
- **可视化分析** — 使用 Matplotlib / Plotly 绘制 K 线图与指标图表
- **回测框架** — 支持简单交易策略的回测与评估

## 技术栈

| 技术 | 用途 |
|------|------|
| Python | 核心开发语言 |
| Pandas | 数据处理与分析 |
| Matplotlib / Plotly | 数据可视化 |
| NumPy | 数值计算 |
| yfinance / tushare | 股票数据源 |

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/Fanhua041027/Stock-Market-Analysis.git
cd Stock-Market-Analysis

# 安装依赖
pip install -r requirements.txt

# 运行分析
python main.py
```

## 许可证

本项目仅供学习研究使用。
