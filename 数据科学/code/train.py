import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import os

# 固定随机种子
np.random.seed(42)

# 模拟训练数据
def generate_sample_data():
    # 生成300只股票的模拟数据
    stock_ids = [f"stock_{i}" for i in range(300)]
    
    # 生成特征数据
    n_samples = 1000
    n_features = 10
    
    X = np.random.randn(n_samples, n_features)
    y = np.random.randn(n_samples)  # 模拟收益率
    
    return stock_ids, X, y

def train_model():
    print("Generating sample data...")
    stock_ids, X, y = generate_sample_data()
    
    print("Training RandomForest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # 保存模型
    os.makedirs('models', exist_ok=True)
    with open('models/model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # 保存股票ID列表
    with open('models/stock_ids.pkl', 'wb') as f:
        pickle.dump(stock_ids, f)
    
    print("Model saved successfully!")

if __name__ == "__main__":
    train_model()