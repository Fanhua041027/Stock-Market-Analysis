# 2026大数据挑战赛 - 基于历史数据预测未来股价收益

## 项目结构

```
├── code/
│   ├── train.py        # 模型训练脚本
│   └── test.py         # 模型测试和结果生成脚本
├── models/             # 模型保存目录
├── Dockerfile          # Docker镜像构建文件
├── requirements.txt    # Python依赖包
├── init.sh             # 环境初始化脚本
├── train.sh            # 训练脚本
├── test.sh             # 测试脚本
└── README.md           # 项目说明文档
```

## 算法说明

本项目使用随机森林回归模型（RandomForestRegressor）来预测股票收益率。

### 算法流程
1. **数据生成**：生成模拟的股票特征数据和收益率数据
2. **模型训练**：使用随机森林模型训练数据
3. **预测**：对测试数据进行收益率预测
4. **选股**：选择预测收益率最高的不超过5只股票
5. **权重分配**：平均分配权重，确保权重之和≤1

### 技术特点
- 固定随机种子（42），确保结果可复现
- 使用随机森林算法，具有较好的预测性能
- 严格按照比赛要求生成result.csv文件

## 环境要求

- Python 3.10
- pandas
- numpy
- scikit-learn

## 运行说明

### 构建Docker镜像
```bash
docker build -t bdc2026 .
```

### 导出Docker镜像
```bash
docker save -o bdc2026.tar bdc2026
```

### 运行流程
1. 初始化环境：`bash init.sh`
2. 训练模型：`bash train.sh`
3. 生成结果：`bash test.sh`

## 输出说明

运行完成后，会在根目录生成`result.csv`文件，格式如下：

```csv
stock_id,weight
stock_250,0.2
stock_100,0.2
stock_50,0.2
stock_150,0.2
stock_200,0.2
```

其中：
- `stock_id`：股票代码
- `weight`：股票权重，权重之和≤1

## 注意事项

1. 本项目使用模拟数据进行训练和测试
2. 实际比赛中需要替换为真实的沪深300成分股数据
3. 确保在断网环境下运行，所有依赖包已打包在Docker镜像中
4. 预测时间控制在5分钟以内，训练时间控制在8小时以内