import pandas as pd
import os

# ✅ 設定根資料夾與條件
root_folder = "./dmepos_files"                # 主資料夾，會遞迴所有子資料夾
keywords = ["DMEPOS", "DMEPEN"]               # 多個關鍵字
valid_extensions = [".csv", ".xlsx"]          # 副檔名限制

# 建立空 DataFrame 用來合併資料
combined_df = pd.DataFrame()

# 遞迴掃描所有子資料夾與檔案
for dirpath, dirnames, filenames in os.walk(root_folder):
    for filename in filenames:
        if any(kw in filename for kw in keywords) and any(filename.endswith(ext) for ext in valid_extensions):
            file_path = os.path.join(dirpath, filename)

            try:
                if filename.endswith(".xlsx"):
                    sheets = pd.read_excel(file_path, sheet_name=None)
                    df = pd.concat(sheets.values(), ignore_index=True)
                elif filename.endswith(".csv"):
                    df = pd.read_csv(file_path)

                combined_df = pd.concat([combined_df, df], ignore_index=True)
                print(f"✅ 已加入：{file_path}")
            except Exception as e:
                print(f"⚠️ 錯誤讀取 {file_path}：{e}")

# 如果完全沒有資料
if combined_df.empty:
    print("❌ 沒有符合條件的檔案，請檢查資料夾或條件。")
    exit()

# 取第 6 列作為欄位標題
header_row_index = 5
column_headers = combined_df.iloc[header_row_index].dropna()
df_cleaned = combined_df.copy()
df_cleaned.columns = combined_df.iloc[header_row_index]
df_cleaned = df_cleaned.iloc[header_row_index + 1:]

# 移除空列與空欄
df_cleaned.dropna(axis=1, how='all', inplace=True)
df_cleaned.dropna(axis=0, how='all', inplace=True)

# 只保留有命名的欄位
df_final = df_cleaned[column_headers.values]

# 輸出結果
df_final.to_csv("Merged_MultiFolder_DMEPOS.csv", index=False)
df_final.to_excel("Merged_MultiFolder_DMEPOS.xlsx", index=False)

print("✅ 所有子資料夾內的符合檔案已成功合併！")
