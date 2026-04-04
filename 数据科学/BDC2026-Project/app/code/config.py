import os

# 基础路径配置 (Docker 环境中必须使用绝对路径)
BASE_DIR = "/app"
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# 数据文件路径
TRAIN_FILE = os.path.join(DATA_DIR, "train.csv")
TEST_FILE = os.path.join(DATA_DIR, "test.csv")
RESULT_FILE = os.path.join(OUTPUT_DIR, "result.csv")
MODEL_FILE = os.path.join(MODEL_DIR, "lgb_model.pkl")

# 模型参数 (冲冠建议：使用较大的树数量和较小的学习率)
PARAMS = {
    "objective": "regression",      # 回归任务
    "metric": "rmse",               # 评估指标
    "boosting_type": "gbdt",        # 梯度提升树
    "num_leaves": 63,               # 叶子节点数
    "learning_rate": 0.01,          # 学习率 (小一点更稳)
    "feature_fraction": 0.8,        # 特征采样
    "bagging_fraction": 0.8,        # 数据采样
    "bagging_freq": 5,              # 采样频率
    "verbose": -1,                  # 关闭日志
    "seed": 42,                     # 固定随机种子 (至关重要！)
    "n_jobs": -1                    # 使用所有CPU核心
}

# 训练参数
EARLY_STOPPING_ROUNDS = 100
NUM_BOOST_ROUND = 2000