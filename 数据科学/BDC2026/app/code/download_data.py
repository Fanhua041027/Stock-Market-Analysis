import baostock as bs
import pandas as pd
import os
from datetime import datetime, timedelta

def download_hs300_data(start_date='2020-01-01', end_date='2024-12-31'):
    """
    下载沪深300成分股的历史日线数据
    """
    # 登录baostock
    lg = bs.login()
    print(f"登录状态: {lg.error_msg}")
    
    # 获取沪深300成分股列表
    rs = bs.query_hs300_stocks()
    hs300_stocks = []
    while (rs.error_code == '0') & rs.next():
        hs300_stocks.append(rs.get_row_data())
    
    hs300_df = pd.DataFrame(hs300_stocks, columns=rs.fields)
    print(f"沪深300成分股数量: {len(hs300_df)}")
    
    # 下载数据
    all_data = []
    for index, row in hs300_df.iterrows():
        code = row['code']
        print(f"正在下载: {code} ({index+1}/{len(hs300_df)})")
        
        # 查询日线数据
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3"  # 不复权
        )
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if data_list:
            df = pd.DataFrame(data_list, columns=rs.fields)
            all_data.append(df)
    
    # 合并数据
    result_df = pd.concat(all_data, ignore_index=True)
    
    # 转换数据类型
    result_df['open'] = pd.to_numeric(result_df['open'], errors='coerce')
    result_df['high'] = pd.to_numeric(result_df['high'], errors='coerce')
    result_df['low'] = pd.to_numeric(result_df['low'], errors='coerce')
    result_df['close'] = pd.to_numeric(result_df['close'], errors='coerce')
    result_df['volume'] = pd.to_numeric(result_df['volume'], errors='coerce')
    
    # 删除空值
    result_df = result_df.dropna()
    
    # 保存数据
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'train.csv')
    result_df.to_csv(output_file, index=False)
    
    print(f"数据已保存到: {output_file}")
    print(f"数据形状: {result_df.shape}")
    print(f"股票数量: {len(result_df['code'].unique())}")
    print(f"日期范围: {result_df['date'].min()} 到 {result_df['date'].max()}")
    
    # 登出baostock
    bs.logout()

def create_test_data():
    """
    创建测试数据（使用训练数据的最后一天）
    """
    train_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'train.csv')
    test_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'test.csv')
    
    # 读取训练数据
    train_df = pd.read_csv(train_file)
    
    # 获取最后一天的数据
    last_date = train_df['date'].max()
    test_df = train_df[train_df['date'] == last_date].copy()
    
    # 保存测试数据
    test_df.to_csv(test_file, index=False)
    
    print(f"测试数据已保存到: {test_file}")
    print(f"测试数据形状: {test_df.shape}")

if __name__ == "__main__":
    print("=== 开始下载沪深300数据 ===")
    download_hs300_data()
    
    print("\n=== 创建测试数据 ===")
    create_test_data()
    
    print("\n=== 数据准备完成 ===")