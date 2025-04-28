import pandas as pd

# === 步驟 1：讀取資料 ===

# 商品價格檔案（含各州欄位）
df = pd.read_csv("Merged_MultiFolder_DMEPOS.csv")

# 美國各州人口檔案（2020 Census）
pop_df = pd.read_csv("us_pop_by_state.csv")

# 州稅率檔案
tax_df_raw = pd.read_excel("2024 Sales Tax Rates State  Local Sales Tax by State.xlsx", sheet_name='Sheet1')

# === 步驟 2：前處理 ===

# 處理商品價格表
price_cols = [col for col in df.columns if '(' in col and ')' in col]
df[price_cols] = df[price_cols].apply(pd.to_numeric, errors='coerce')

# 建立人口對應字典
state_to_pop = dict(zip(pop_df['state'], pop_df['2020_census']))

# 正確整理稅率表
tax_df = tax_df_raw.iloc[1:].copy()
tax_df.columns = ['State', 'State Tax Rate', 'State Rank', 'Avg Local Tax Rate', 'Combined Rate', 'Combined Rank', 'Max Local Tax Rate']

state_to_tax = dict(zip(tax_df['State'], tax_df['Combined Rate']))

# 州縮寫對應全名（手動對應表）
abbr_to_state = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts",
    "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri", "MT": "Montana",
    "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico",
    "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota",
    "TN": "Tennessee", "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia"
}

# 建立欄位名對應州名
col_to_state_name = {}
for col in price_cols:
    abbr = col.split()[0]
    if abbr in abbr_to_state:
        col_to_state_name[col] = abbr_to_state[abbr]

# === 步驟 3：計算加稅後的加權平均價格 ===

weighted_prices = []
for idx, row in df.iterrows():
    weighted_sum = 0
    total_weight = 0
    for col, state_name in col_to_state_name.items():
        price = row[col]
        pop = state_to_pop.get(state_name)
        tax_rate = state_to_tax.get(state_name, 0)

        if pd.notnull(price) and pop is not None:
            adjusted_price = price * (1 + tax_rate)
            weighted_sum += adjusted_price * pop
            total_weight += pop
    weighted_price = weighted_sum / total_weight if total_weight > 0 else None
    weighted_prices.append(weighted_price)

# 將結果加入資料表中
df['US_Weighted_Price_with_Tax'] = weighted_prices

# 儲存成新檔案
df.to_csv("DMEPOS_with_US_Weighted_Price_with_Tax.csv", index=False)

# 顯示前幾筆結果供檢查
print(df[['HCPCS', 'Description', 'US_Weighted_Price_with_Tax']].head())
