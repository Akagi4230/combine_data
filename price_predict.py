import pandas as pd

# 讀取資料
df = pd.read_csv('./DMEPOS_with_US_Weighted_Prices.csv')

# 顯示欄位資訊
print(df.columns.tolist())

# 預覽資料
print(df.tail())
# 假設最後兩欄是要預測的欄位
target_cols = df.columns[-2:]

# 找出可當作特徵的欄位（去掉目標欄位）
feature_cols = [col for col in df.columns if col not in target_cols]

# 分開特徵與標籤
X = df[feature_cols]
y = df[target_cols]

# 將非數值欄位轉換（Label Encoding 或 One-hot）
X = pd.get_dummies(X, drop_first=True)

# 處理缺失值（簡單方法）
X = X.fillna(0)
y = y.fillna(0)
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 分訓練與測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 建立並訓練模型（同時預測兩欄）
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 預測
y_pred = model.predict(X_test)

# 評估
mae = mean_absolute_error(y_test, y_pred)
print(f"MAE 平均絕對誤差：{mae:.2f}")
# 將預測結果轉為 DataFrame（與 y_test 結構一致）
pred_df = pd.DataFrame(y_pred, columns=y.columns, index=y_test.index)

# 合併實際與預測值，方便比對
result_df = pd.concat([y_test.reset_index(drop=True), pred_df.reset_index(drop=True)], axis=1)
result_df.columns = [f"actual_{col}" for col in y.columns] + [f"pred_{col}" for col in y.columns]

# 輸出結果為 CSV 檔案
result_df.to_csv("price_prediction_result.csv", index=False)
print("✅ 預測結果已儲存為 price_prediction_result.csv")