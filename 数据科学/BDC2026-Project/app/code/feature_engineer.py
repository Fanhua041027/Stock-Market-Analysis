import pandas as pd
import numpy as np
from scipy.stats import zscore

def winsorize(series, limits=(0.025, 0.975)):
    """去极值：将超过 2.5% 和 97.5% 分位数的值拉回到边界"""
    if series.empty: return series
    low, high = series.quantile(limits)
    return series.clip(lower=low, upper=high)

def generate_features(df):
    """
    输入: 原始 DataFrame
    输出: 处理后的 DataFrame
    """
    # 1. 基础预处理
    df = df.sort_values(['code', 'date'])
    
    # 2. 基础因子计算 (向量化，极速)
    # 动量因子
    df['mom_5'] = df.groupby('code')['close'].pct_change(5)
    df['mom_10'] = df.groupby('code')['close'].pct_change(10)
    
    # 波动率因子 (使用对数收益率的标准差)
    df['log_ret'] = np.log(df['close'] / df['close'].shift(1))
    df['vol_20'] = df.groupby('code')['log_ret'].transform(lambda x: x.rolling(20).std())
    
    # 价量关系 (量价齐升)
    df['vol_price_corr'] = df.groupby('code').apply(lambda x: x['volume'].rolling(10).corr(x['close'])).values
    
    # 3. 数据清洗与去极值
    # 填充 NaN (用 0 或前值填充，防止模型报错)
    df = df.fillna(0)
    
    # 对关键因子进行去极值
    factor_cols = ['mom_5', 'mom_10', 'vol_20', 'vol_price_corr']
    for col in factor_cols:
        if col in df.columns:
            df[col] = df.groupby('date')[col].transform(winsorize)
            
    return df

def prepare_data(df, is_train=True):
    """
    准备 X, y
    """
    # 选取特征
    feature_cols = ['mom_5', 'mom_10', 'vol_20', 'vol_price_corr', 'open', 'high', 'low', 'close', 'volume']
    feature_cols = [c for c in feature_cols if c in df.columns]
    
    X = df[feature_cols].copy()
    
    # 简单的标准化 (让模型收敛更快)
    # 注意：实战中应该用训练集的均值方差来标准化测试集，这里为了简化先做全局标准化
    # 严谨做法需在 train.py 中保存 scaler
    X = X.replace([np.inf, -np.inf], 0) # 处理无穷大
    
    if is_train:
        y = df['label']
        return X, y
    else:
        return X