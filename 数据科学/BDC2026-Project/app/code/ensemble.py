import pandas as pd
import numpy as np
import pickle
import os
import config
from feature_engineer import generate_features, prepare_data

class EnsembleModel:
    """
    集成学习模型：融合多个模型的预测结果
    """
    def __init__(self):
        self.models = []
        self.weights = []
    
    def add_model(self, model_path, weight=1.0):
        """
        添加模型到集成中
        """
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        self.models.append(model)
        self.weights.append(weight)
    
    def predict(self, X):
        """
        集成预测
        """
        predictions = []
        for model in self.models:
            pred = model.predict(X)
            predictions.append(pred)
        
        # 加权平均
        weighted_pred = np.zeros_like(predictions[0])
        total_weight = sum(self.weights)
        
        for pred, weight in zip(predictions, self.weights):
            weighted_pred += pred * (weight / total_weight)
        
        return weighted_pred

def train_catboost_model(X_train, y_train, X_val, y_val):
    """
    训练CatBoost模型
    """
    from catboost import CatBoostRegressor
    
    model = CatBoostRegressor(
        iterations=2000,
        learning_rate=0.01,
        depth=6,
        loss_function='RMSE',
        eval_metric='RMSE',
        random_seed=42,
        verbose=False
    )
    
    model.fit(
        X_train, y_train,
        eval_set=(X_val, y_val),
        early_stopping_rounds=100
    )
    
    return model

def main():
    """
    训练集成模型
    """
    print("=== 开始训练集成模型 ===")
    
    # 1. 读取数据
    df = pd.read_csv(config.TRAIN_FILE)
    
    # 2. 构造标签
    df['future_close_5'] = df.groupby('code')['open'].shift(-5)
    df['future_close_4'] = df.groupby('code')['open'].shift(-4)
    df['target_price'] = df['future_close_5'].fillna(df['future_close_4'])
    df['label'] = (df['target_price'] - df['open']) / df['open']
    df = df.dropna(subset=['label'])
    
    # 3. 特征工程
    df = generate_features(df)
    
    # 4. 准备数据
    X, y = prepare_data(df, is_train=True)
    
    # 5. 时间序列切分
    split_point = int(len(X) * 0.8)
    X_train, X_val = X.iloc[:split_point], X.iloc[split_point:]
    y_train, y_val = y.iloc[:split_point], y.iloc[split_point:]
    
    # 6. 训练CatBoost模型
    print("训练CatBoost模型...")
    catboost_model = train_catboost_model(X_train, y_train, X_val, y_val)
    
    # 7. 保存CatBoost模型
    catboost_model_path = os.path.join(config.MODEL_DIR, "catboost_model.pkl")
    os.makedirs(config.MODEL_DIR, exist_ok=True)
    with open(catboost_model_path, 'wb') as f:
        pickle.dump(catboost_model, f)
    
    print("=== 集成模型训练完成 ===")

if __name__ == "__main__":
    main()