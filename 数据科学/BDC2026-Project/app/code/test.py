import pandas as pd
import lightgbm as lgb
import pickle
import config
from feature_engineer import generate_features, prepare_data

def main():
    print("=== 开始预测 ===")
    
    # 1. 加载模型
    try:
        with open(config.MODEL_FILE, 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("错误：未找到模型文件，请先运行 train.sh")
        return

    # 2. 读取测试数据和训练数据（用于历史窗口）
    # 实现"全量拼接"计算法，解决测试集历史窗口不足的问题
    try:
        print("读取训练数据作为历史背景...")
        train_df = pd.read_csv(config.TRAIN_FILE)
        print("读取测试数据...")
        test_df = pd.read_csv(config.TEST_FILE)
    except FileNotFoundError as e:
        print(f"错误：未找到数据文件: {e}")
        return
    
    # 拼接训练和测试数据
    print("拼接数据...")
    df = pd.concat([train_df, test_df], ignore_index=True)
    
    # 3. 特征工程
    print("进行特征工程...")
    df = generate_features(df)
    
    # 筛选出测试数据
    test_dates = test_df['date'].unique()
    df = df[df['date'].isin(test_dates)]
    print(f"筛选后测试数据形状: {df.shape}")
    
    # 4. 准备特征
    X = prepare_data(df, is_train=False)
    X = X.fillna(0) # 再次确保无 NaN
    
    # 5. 预测
    # 确保 X 的列顺序与训练时一致
    # 注意：如果特征列缺失，需要补齐
    try:
        preds = model.predict(X)
    except Exception as e:
        print(f"预测出错: {e}")
        return

    # 6. 构建投资组合
    df['pred_ret'] = preds
    
    # 排序
    df = df.sort_values('pred_ret', ascending=False)
    
    # 【优化策略】：简单的 Top 5 选取
    # 为了速度，这里不再计算复杂的相关性矩阵
    # 如果担心行业集中，可以在这里加入简单的行业去重逻辑（如果有行业数据）
    # 这里采用最稳健的策略：直接取预测分最高的 5 只
    top5 = df.head(5)
    
    # 兜底：如果不足 5 只，有多少选多少
    if len(top5) == 0:
        print("警告：没有选出股票，随机选择 5 只")
        top5 = df.sample(min(5, len(df)))
    
    # 7. 生成结果
    result = top5[['code']].copy()
    result['weight'] = 1.0 / len(top5) # 等权
    
    # 格式化代码 (确保是 6 位字符串)
    result['code'] = result['code'].astype(int).apply(lambda x: f"{x:06d}")
    
    # 保存
    result.to_csv(config.RESULT_FILE, index=False)
    
    print(f"=== 预测结束，选出 {len(result)} 只股票 ===")

if __name__ == "__main__":
    main()