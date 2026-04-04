import pandas as pd
import lightgbm as lgb
import pickle
import config

def main():
    print("=== 验证LambdaRank模型 ===")
    
    # 1. 加载模型
    try:
        with open(config.MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("错误：未找到模型文件，请先运行 train.py")
        return
    
    # 2. 检查模型参数
    print("\n模型参数:")
    print(f"  objective: {model.params.get('objective', 'N/A')}")
    print(f"  metric: {model.params.get('metric', 'N/A')}")
    print(f"  ndcg_at: {model.params.get('ndcg_at', 'N/A')}")
    
    # 3. 读取测试数据
    try:
        df = pd.read_csv(config.TEST_FILE)
    except FileNotFoundError:
        print("错误：未找到测试数据")
        return
    
    # 4. 简单特征工程
    df['pct_change'] = df.groupby('code')['close'].pct_change()
    df['volatility'] = df.groupby('code')['close'].transform(lambda x: x.rolling(20).std())
    df['volume_change'] = df.groupby('code')['volume'].pct_change()
    df = df.fillna(0)
    
    # 5. 准备特征
    feature_cols = ['open', 'high', 'low', 'close', 'volume', 'pct_change', 'volatility', 'volume_change']
    X = df[feature_cols]
    
    # 6. 预测
    preds = model.predict(X)
    
    # 7. 显示预测结果
    df['pred_score'] = preds
    df_sorted = df.sort_values('pred_score', ascending=False)
    
    print("\n预测结果排序:")
    print(df_sorted[['code', 'pred_score']].head(10))
    
    print("\n=== 验证完成 ===")

if __name__ == "__main__":
    main()