import pandas as pd
import numpy as np
import os
import config

def generate_sample_data(file_path, n_stocks=300, n_days=1000):
    """生成模拟数据"""
    # 生成股票代码
    stock_codes = [f"{i:06d}" for i in range(1, n_stocks + 1)]
    
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
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume
            })
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 保存数据
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)
    
    print(f"模拟数据已生成并保存到 {file_path}")
    print(f"数据形状: {df.shape}")
    print(f"股票数量: {len(df['code'].unique())}")
    print(f"日期范围: {df['date'].min()} 到 {df['date'].max()}")

if __name__ == "__main__":
    # 生成训练数据
    generate_sample_data(config.TRAIN_FILE)
    
    # 生成测试数据
    generate_sample_data(config.TEST_FILE, n_days=10)