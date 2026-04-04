import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据路径
DATA_DIR = os.path.join(BASE_DIR, 'data')
TRAIN_FILE = os.path.join(DATA_DIR, 'train.csv')
TEST_FILE = os.path.join(DATA_DIR, 'test.csv')

# 模型路径
MODEL_DIR = os.path.join(BASE_DIR, 'model')
MODEL_FILE = os.path.join(MODEL_DIR, 'model.pkl')

# 输出路径
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')
RESULT_FILE = os.path.join(OUTPUT_DIR, 'result.csv')

# 模型参数
PARAMS = {
    "objective": "regression",
    "metric": "rmse",
    "boosting_type": "gbdt",
    "num_leaves": 63,
    "learning_rate": 0.01,
    "feature_fraction": 0.8,
    "bagging_fraction": 0.8,
    "bagging_freq": 5,
    "verbose": -1,
    "seed": 42,
    "n_jobs": -1
}

# 训练参数
EARLY_STOPPING_ROUNDS = 100
NUM_BOOST_ROUND = 10000