import pandas as pd
import lightgbm as lgb
import pickle
import config
import os

def main():
    print("=== 开始预测 ===")
    
    # 1. 加载模型
    try:
        with open(config.MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("错误：未找到模型文件，请先运行 train.py")
        return

    # 2. 读取测试数据
    try:
        df = pd.read_csv(config.TEST_FILE)
    except FileNotFoundError:
        print("错误：未找到测试数据")
        return
    
    # 3. 特征工程 (必须与训练时完全一致)
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
    
    # 4. 准备特征
    feature_cols = ['open', 'high', 'low', 'close', 'volume', 
                   'pct_change', 'volatility', 'volume_change',
                   'ret_7d', 'vol_7d', 'bias_7']
    X = df[feature_cols]
    
    # 5. 预测
    print("正在进行预测...")
    preds = model.predict(X)
    
    # 6. 构建投资组合
    df['pred_score'] = preds
    
    # 按照预测分数排序
    df = df.sort_values('pred_score', ascending=False)
    
    # 选择 Top 5 股票
    top5 = df.head(5)
    
    # 7. 生成结果
    result = pd.DataFrame({
        'code': top5['code'].apply(lambda x: f"{int(x):06d}"),
        'weight': 1.0 / len(top5)  # 等权
    })
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(config.RESULT_FILE), exist_ok=True)
    
    # 保存结果
    result.to_csv(config.RESULT_FILE, index=False)
    
    print(f"=== 预测结束，选出 {len(result)} 只股票 ===")
    print(f"结果已保存到: {config.RESULT_FILE}")
    print("\n选出的股票:")
    print(result)

if __name__ == "__main__":
    main()