import pandas as pd
import lightgbm as lgb
import pickle
import config
import os

def main():
    print("=== 开始训练 ===")
    
    # 1. 读取数据
    try:
        df = pd.read_csv(config.TRAIN_FILE)
    except FileNotFoundError:
        print("错误：未找到训练数据")
        return
    
    # 2. 构造标签 (Label) - 预测未来7天的收益率
    print("生成标签：预测未来7天收益率...")
    
    # 获取 7天后的收盘价
    df['close_7_days_later'] = df.groupby('code')['close'].shift(-7)
    
    # 计算未来7天的涨跌幅 (收益率)
    # 公式：(未来价格 - 当前价格) / 当前价格
    df['label_return'] = (df['close_7_days_later'] - df['close']) / df['close']
    
    # 去除因 shift 产生的 NaN (最后7天的数据)
    df = df.dropna(subset=['label_return'])
    
    # 3. 标签分箱 (LambdaRank 要求标签为整数)
    # 将连续的收益率切分为 5 个等级 (0, 1, 2, 3, 4)
    # 4 代表未来7天涨得最多，0 代表跌得最多
    print("进行标签分箱...")
    df['label_bin'] = pd.qcut(df['label_return'], q=5, labels=False, duplicates='drop')
    
    # 4. 特征工程 - 添加7天周期的特征
    print("正在生成特征...")
    
    # 基础特征
    df['pct_change'] = df.groupby('code')['close'].pct_change()
    df['volatility'] = df.groupby('code')['close'].transform(lambda x: x.rolling(20).std())
    df['volume_change'] = df.groupby('code')['volume'].pct_change()
    
    # 7天周期的特征
    # 1. 7日收益率 (Momentum)
    df['ret_7d'] = df.groupby('code')['close'].pct_change(7)
    
    # 2. 7日波动率 (Volatility)
    # 过去7天的收益率标准差
    df['vol_7d'] = df.groupby('code')['close'].pct_change().rolling(7).std().reset_index(level=0, drop=True)
    
    # 3. 均线乖离 (距离7日均线的距离)
    df['ma_7'] = df.groupby('code')['close'].transform(lambda x: x.rolling(7).mean())
    df['bias_7'] = (df['close'] - df['ma_7']) / df['ma_7']
    
    # 填充 NaN
    df = df.fillna(0)
    
    # 5. 准备数据
    feature_cols = ['open', 'high', 'low', 'close', 'volume', 
                   'pct_change', 'volatility', 'volume_change',
                   'ret_7d', 'vol_7d', 'bias_7']
    
    # 6. 时序切分 (防止未来函数)
    # 假设数据已经按时间排序，取最后 20% 作为验证集
    split_idx = int(len(df) * 0.8)
    df_train = df.iloc[:split_idx].copy()
    df_val = df.iloc[split_idx:].copy()
    
    print(f"训练集大小: {len(df_train)}, 验证集大小: {len(df_val)}")
    
    # 7. 准备分组信息 (LambdaRank 关键)
    # LambdaRank 需要知道哪些数据属于同一个"查询"
    # 在量化里，每一天就是一个查询（我们要对当天的股票排序）
    
    # 确保数据按日期排序
    df_train = df_train.sort_values('date')
    df_val = df_val.sort_values('date')
    
    # 统计每天的股票数量
    query_groups_train = df_train.groupby('date').size().tolist()
    query_groups_val = df_val.groupby('date').size().tolist()
    
    print(f"训练集查询组数: {len(query_groups_train)}, 验证集查询组数: {len(query_groups_val)}")
    
    # 准备特征和标签
    X_train = df_train[feature_cols]
    y_train = df_train['label_bin']  # 使用分箱后的标签
    X_val = df_val[feature_cols]
    y_val = df_val['label_bin']  # 使用分箱后的标签
    
    # 8. 构建 LightGBM 数据集
    # 关键：必须传入 group 参数！
    train_set = lgb.Dataset(X_train, y_train, group=query_groups_train)
    val_set = lgb.Dataset(X_val, y_val, group=query_groups_val, reference=train_set)
    
    # 9. 训练模型 - 使用 LambdaRank 损失函数
    params = {
        'objective': 'lambdarank',    # 核心：告诉模型我们要排序
        'metric': 'ndcg',             # 核心：用NDCG作为评估标准
        'ndcg_at': [5],               # 重点优化前5名的排序
        'num_leaves': 63,             # 树叶子数
        'learning_rate': 0.05,        # 学习率
        'feature_fraction': 0.8,      # 特征采样
        'bagging_fraction': 0.8,      # 数据采样
        'bagging_freq': 5,            # 采样频率
        'verbose': -1,                # 关闭冗余日志
        'seed': 42,                   # 随机种子
        'label_gain': [0, 1, 2, 3, 4]  # 标签增益（对应5个档位：0-4）
    }
    
    model = lgb.train(
        params,
        train_set,
        num_boost_round=2000,         # 迭代次数
        valid_sets=[val_set],
        callbacks=[lgb.early_stopping(100), lgb.log_evaluation(period=100)]
    )
    
    # 10. 保存模型
    os.makedirs(os.path.dirname(config.MODEL_FILE), exist_ok=True)
    with open(config.MODEL_FILE, 'wb') as f:
        pickle.dump(model, f)
        
    print("=== 训练结束 ===")

if __name__ == "__main__":
    main()