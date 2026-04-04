import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import os

class FeatureEngineer:
    def __init__(self):
        self.scaler = StandardScaler()
        
    def calculate_lag_features(self, df, lags=[1, 5, 10]):
        """计算滞后特征"""
        for col in ['open', 'high', 'low', 'close', 'volume']:
            for lag in lags:
                df[f'{col}_lag_{lag}'] = df[col].shift(lag)
        return df
    
    def calculate_rolling_features(self, df, windows=[5, 10, 20, 60]):
        """计算滚动窗口特征"""
        for col in ['open', 'high', 'low', 'close', 'volume']:
            for window in windows:
                df[f'{col}_roll_{window}_mean'] = df[col].rolling(window).mean()
                df[f'{col}_roll_{window}_std'] = df[col].rolling(window).std()
                df[f'{col}_roll_{window}_skew'] = df[col].rolling(window).skew()
                df[f'{col}_roll_{window}_kurt'] = df[col].rolling(window).kurt()
        return df
    
    def calculate_alpha_factors(self, df):
        """计算WorldQuant 101 Alpha因子"""
        # Alpha 1: -1 * correlation(rank(open), rank(volume), 10)
        df['alpha_1'] = -1 * df['open'].rank().rolling(10).corr(df['volume'].rank())
        
        # Alpha 2: delta(log(close), 2)
        df['alpha_2'] = np.log(df['close']).diff(2)
        
        # Alpha 3: rank(open) - rank(close)
        df['alpha_3'] = df['open'].rank() - df['close'].rank()
        
        # Alpha 4: rank(high) - rank(low)
        df['alpha_4'] = df['high'].rank() - df['low'].rank()
        
        # Alpha 5: volume / mean(volume, 20)
        df['alpha_5'] = df['volume'] / df['volume'].rolling(20).mean()
        
        return df
    
    def calculate_market_relative_features(self, df, market_df):
        """计算相对于大盘的特征"""
        # 确保时间索引一致
        df = df.merge(market_df[['close']], left_index=True, right_index=True, suffixes=('', '_market'))
        
        # 计算超额收益
        df['excess_return'] = df['close'].pct_change() - df['close_market'].pct_change()
        
        # 计算Beta值（简单线性回归斜率）
        returns = df['close'].pct_change().dropna()
        market_returns = df['close_market'].pct_change().dropna()
        
        if len(returns) > 0 and len(market_returns) > 0:
            beta = np.cov(returns, market_returns)[0, 1] / np.var(market_returns)
            df['beta'] = beta
        else:
            df['beta'] = 1.0
        
        return df
    
    def generate_labels(self, df, is_holiday=False):
        """生成标签"""
        # 计算T+1到T+5的收益率
        if is_holiday:
            # A阶段T+5复用T+4
            df['label'] = (df['open'].shift(-4) - df['open'].shift(-1)) / df['open'].shift(-1)
        else:
            df['label'] = (df['open'].shift(-5) - df['open'].shift(-1)) / df['open'].shift(-1)
        return df
    
    def fit_transform(self, df, market_df=None):
        """拟合并转换特征"""
        # 计算基础特征
        df = self.calculate_lag_features(df)
        df = self.calculate_rolling_features(df)
        df = self.calculate_alpha_factors(df)
        
        # 计算市场相关特征
        if market_df is not None:
            df = self.calculate_market_relative_features(df, market_df)
        
        # 生成标签
        df = self.generate_labels(df)
        
        # 移除NaN值
        df = df.dropna()
        
        # 分离特征和标签
        features = df.drop(['label'], axis=1)
        labels = df['label']
        
        # 标准化特征
        features_scaled = self.scaler.fit_transform(features)
        
        # 保存scaler
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.scaler, 'models/scaler.pkl')
        
        return features_scaled, labels
    
    def transform(self, df, market_df=None):
        """转换特征"""
        # 计算基础特征
        df = self.calculate_lag_features(df)
        df = self.calculate_rolling_features(df)
        df = self.calculate_alpha_factors(df)
        
        # 计算市场相关特征
        if market_df is not None:
            df = self.calculate_market_relative_features(df, market_df)
        
        # 移除NaN值
        df = df.dropna()
        
        # 标准化特征
        features_scaled = self.scaler.transform(df)
        
        return features_scaled
    
    def load_scaler(self):
        """加载scaler"""
        self.scaler = joblib.load('models/scaler.pkl')
        return self