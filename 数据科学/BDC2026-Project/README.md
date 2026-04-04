# 2026大数据挑战赛参赛代码说明

## 1. 环境配置
- Python: 3.9.18
- LightGBM: 4.3.0
- 其他: numpy, pandas, scikit-learn, joblib

## 2. 项目结构
```
BDC2026-Project/
├── app/
│   ├── code/                 # 存放所有Python代码
│   │   ├── train.py          # 训练脚本
│   │   ├── test.py           # 预测脚本 (核心：生成result.csv)
│   │   ├── feature_engineer.py # 特征工程
│   │   ├── config.py         # 配置文件 (路径、参数)
│   │   ├── generate_sample_data.py # 生成模拟数据脚本
│   │   └── requirements.txt  # 依赖库列表
│   ├── data/                 # 挂载点：存放CSV数据
│   │   ├── train.csv         # 训练数据文件
│   │   └── test.csv          # 测试数据文件
│   ├── model/                # 挂载点：存放训练好的模型文件
│   ├── output/               # 挂载点：必须生成 result.csv 在此
│   ├── temp/                 # 挂载点：存放中间处理数据
│   ├── init.sh               # 初始化脚本
│   ├── train.sh              # 训练启动脚本
│   └── test.sh               # 预测启动脚本
├── docker-compose.yml        # Docker Compose配置文件
├── Dockerfile                # Docker镜像构建文件
└── README.md                 # 比赛要求的说明文档
```

## 3. 快速开始

### 3.1 生成模拟数据
如果没有真实数据，可以运行以下命令生成模拟数据：

```bash
# 进入项目目录
cd BDC2026-Project

# 运行模拟数据生成脚本
python app/code/generate_sample_data.py
```

这将在 `app/data/` 目录下生成 `train.csv` 和 `test.csv` 文件。

### 3.2 构建Docker镜像
```bash
# 构建镜像
docker build -t bdc2026 .
```

### 3.3 运行训练
```bash
# 运行训练
docker-compose run bdc2026 bash train.sh
```

### 3.4 运行预测
```bash
# 运行预测
docker-compose run bdc2026 bash test.sh
```

预测结果将保存在 `app/output/result.csv` 文件中。

## 4. 算法说明

### 4.1 特征工程
- **动量因子**：mom_5, mom_10
- **波动率因子**：vol_20
- **成交量因子**：vol_change
- **技术指标**：rsi_14
- **日内波动特征**：intraday_volatility
- **市场情绪**：market_breadth (上涨家数/下跌家数)
- **高阶交互特征**：volume_price_interaction
- **时序统计特征**：skew_20, kurt_20
- **行业中性化**：industry_neutral_close
- **基础量价数据**：open, high, low, close, volume

### 4.2 模型训练
- **损失函数**：使用 LambdaRank 损失函数优化 Top-N 排序指标
- **模型选择**：LightGBM + CatBoost 集成学习
- **固定随机种子**：确保可复现性
- **早停策略**：防止过拟合
- **时间序列切分**：避免数据泄露

### 4.3 投资组合构建
- **相关性惩罚**：避免选出高度相关的股票
- **风险平价加权**：权重 ∝ 预测收益率 / 风险
- **过滤负收益**：只选择预测收益为正的股票
- **权重归一化**：确保权重和不超过1

## 5. 免责声明
本模型使用了 LambdaRank 损失函数以优化 Top-N 排序指标，并使用了行业中性化预处理。主要贡献在于机器学习算法的设计与优化，符合比赛要求。

## 6. 注意事项
- 所有依赖包已在Docker镜像构建阶段安装，确保断网运行
- 固定随机种子，确保结果可复现
- 预测时间控制在5分钟以内
- 训练时间控制在8小时以内
- 权重和不超过1
- 股票代码格式为6位数字
- 保存CSV时使用UTF-8编码，无BOM头

## 6. 提交说明
1. 构建Docker镜像：`docker build -t bdc2026 .`
2. 导出Docker镜像：`docker save -o bdc2026.tar bdc2026`
3. 将 `bdc2026.tar` 上传至夸克网盘，生成分享链接
4. 运行预测脚本生成 `result.csv`
5. 提交 `result.csv` 和Docker镜像分享链接

## 7. 冲冠策略
- **特征工程**：添加更多技术指标和基本面因子
- **模型优化**：尝试不同的模型参数，使用集成学习
- **特征选择**：使用LightGBM的特征重要性进行特征选择
- **调参**：使用网格搜索或贝叶斯优化调参
- **风控**：添加风险控制措施，如最大回撤限制

祝参赛成功！