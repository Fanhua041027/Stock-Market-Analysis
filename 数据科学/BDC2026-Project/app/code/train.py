import pandas as pd
import lightgbm as lgb
import pickle
import config
from feature_engineer import generate_features, prepare_data

def main():
    print("=== 开始训练 ===")
    
    # 1. 读取数据
    df = pd.read_csv(config.TRAIN_FILE)
    
    # 2. 构造标签 (Label) - 兼容 A 阶段假期逻辑
    # 获取 T+5 和 T+4 的开盘价
    df['future_5'] = df.groupby('code')['open'].shift(-5)
    df['future_4'] = df.groupby('code')['open'].shift(-4)
    
    # 核心逻辑：优先用 T+5，如果 T+5 缺失（假期），则用 T+4
    df['target_price'] = df['future_5'].fillna(df['future_4'])
    
    # 计算收益率
    df['label'] = (df['target_price'] - df['open']) / df['open']
    
    # 去除因 shift 产生的 NaN (首尾数据)
    df = df.dropna(subset=['label'])
    
    # 3. 特征工程
    print("正在生成特征...")
    df = generate_features(df)
    
    # 4. 准备数据
    X, y = prepare_data(df, is_train=True)
    
    # 5. 时序切分 (防止未来函数)
    # 假设数据已经按时间排序，取最后 20% 作为验证集
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_val = y.iloc[:split_idx], y.iloc[split_idx:]
    
    print(f"训练集大小: {len(X_train)}, 验证集大小: {len(X_val)}")
    
    # 6. 训练模型
    train_set = lgb.Dataset(X_train, label=y_train)
    val_set = lgb.Dataset(X_val, label=y_val, reference=train_set)
    
    # 使用 LambdaRank 损失函数 (直接优化排序)
    params = config.PARAMS.copy()
    params['objective'] = 'lambdarank'
    params['metric'] = 'ndcg'
    params['ndcg_at'] = [5] # 关注 Top 5
    
    model = lgb.train(
        params,
        train_set,
        num_boost_round=config.NUM_BOOST_ROUND,
        valid_sets=[val_set],
        callbacks=[lgb.early_stopping(config.EARLY_STOPPING_ROUNDS), lgb.log_evaluation(period=500)]
    )
    
    # 7. 保存模型
    with open(config.MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
        
    print("=== 训练结束 ===")

if __name__ == "__main__":
    main()