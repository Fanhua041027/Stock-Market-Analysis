import pandas as pd
import numpy as np
import os

def generate_realistic_test_data(n_stocks=50, n_days=500):
    """
    生成包含真实股票代码格式的测试数据
    """
    # 生成真实的股票代码格式
    # 沪市股票：600xxx, 601xxx, 603xxx
    # 深市股票：000xxx, 001xxx, 002xxx, 003xxx
    # 创业板：300xxx
    
    stock_codes = []
    
    # 沪市股票
    for i in range(1, 21):
        stock_codes.append(f"600{i:03d}")
    
    # 深市股票
    for i in range(1, 21):
        stock_codes.append(f"000{i:03d}")
    
    # 创业板股票
    for i in range(1, 11):
        stock_codes.append(f"300{i:03d}")
    
    # 生成日期
    dates = pd.date_range('2020-01-01', periods=n_days, freq='B')
    
    # 生成数据
    data = []
    for code in stock_codes:
        # 生成基础价格
        base_price = np.random.uniform(10, 100)
        price = base_price
        
        for date in dates:
            # 生成每日价格波动
            change = np.random.normal(0, 0.02)  # 每日收益率均值为0，标准差为2%
            price *= (1 + change)
            
            open_price = price * np.random.uniform(0.99, 1.01)
            high_price = max(open_price, price * np.random.uniform(1.0, 1.03))
            low_price = min(open_price, price * np.random.uniform(0.97, 1.0))
            close_price = price
            volume = np.random.uniform(100000, 10000000)
            
            data.append({
                'code': code,
                'date': date.strftime('%Y-%m-%d'),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': int(volume)
            })
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存训练数据
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    train_file = os.path.join(output_dir, 'train.csv')
    df.to_csv(train_file, index=False)
    
    print(f"训练数据已保存到: {train_file}")
    print(f"数据形状: {df.shape}")
    print(f"股票数量: {len(df['code'].unique())}")
    print(f"日期范围: {df['date'].min()} 到 {df['date'].max()}")
    
    # 创建测试数据（最后一天）
    last_date = df['date'].max()
    test_df = df[df['date'] == last_date].copy()
    
    test_file = os.path.join(output_dir, 'test.csv')
    test_df.to_csv(test_file, index=False)
    
    print(f"\n测试数据已保存到: {test_file}")
    print(f"测试数据形状: {test_df.shape}")
    
    # 显示部分股票代码
    print(f"\n股票代码示例:")
    print(df['code'].unique()[:10])

if __name__ == "__main__":
    print("=== 生成包含真实股票代码格式的测试数据 ===")
    generate_realistic_test_data()
    print("\n=== 数据生成完成 ===")