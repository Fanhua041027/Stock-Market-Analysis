import pandas as pd
import os

def fix_stock_codes():
    """
    修复股票代码格式，去掉sh.和sz.前缀
    """
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    # 修复train.csv
    train_file = os.path.join(data_dir, 'train.csv')
    if os.path.exists(train_file):
        train_df = pd.read_csv(train_file)
        train_df['code'] = train_df['code'].astype(str).str.replace('sh.', '').str.replace('sz.', '')
        train_df.to_csv(train_file, index=False)
        print(f"已修复 train.csv，股票代码示例：{train_df['code'].unique()[:5]}")
    
    # 修复test.csv
    test_file = os.path.join(data_dir, 'test.csv')
    if os.path.exists(test_file):
        test_df = pd.read_csv(test_file)
        test_df['code'] = test_df['code'].astype(str).str.replace('sh.', '').str.replace('sz.', '')
        test_df.to_csv(test_file, index=False)
        print(f"已修复 test.csv，股票代码示例：{test_df['code'].unique()[:5]}")

if __name__ == "__main__":
    print("=== 开始修复股票代码格式 ===")
    fix_stock_codes()
    print("=== 修复完成 ===")