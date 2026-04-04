import numpy as np
import pandas as pd
import pickle
import os

# 固定随机种子
np.random.seed(42)

def load_model():
    with open('models/model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('models/stock_ids.pkl', 'rb') as f:
        stock_ids = pickle.load(f)
    
    return model, stock_ids

def generate_test_data(n_stocks, n_features):
    return np.random.randn(n_stocks, n_features)

def generate_result():
    print("Loading model...")
    model, stock_ids = load_model()
    
    print("Generating test data...")
    n_stocks = len(stock_ids)
    n_features = 10
    X_test = generate_test_data(n_stocks, n_features)
    
    print("Predicting returns...")
    predictions = model.predict(X_test)
    
    # 创建股票ID和预测收益率的DataFrame
    stock_returns = pd.DataFrame({
        'stock_id': stock_ids,
        'predicted_return': predictions
    })
    
    # 按预测收益率降序排序
    stock_returns = stock_returns.sort_values('predicted_return', ascending=False)
    
    # 选择前5只股票
    top_stocks = stock_returns.head(5)
    
    # 分配权重（简单平均）
    n_selected = len(top_stocks)
    if n_selected > 0:
        weight = 1.0 / n_selected
        top_stocks['weight'] = weight
    else:
        top_stocks['weight'] = 0.0
    
    # 确保权重之和≤1
    total_weight = top_stocks['weight'].sum()
    if total_weight > 1.0:
        top_stocks['weight'] = top_stocks['weight'] / total_weight
    
    # 生成result.csv
    result = top_stocks[['stock_id', 'weight']]
    result.to_csv('result.csv', index=False)
    
    print("result.csv generated successfully!")
    print(f"Selected {n_selected} stocks with total weight: {total_weight:.4f}")

if __name__ == "__main__":
    generate_result()