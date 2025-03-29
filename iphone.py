import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re

# Disclaimer
"""
This tool is for personal research and comparison only. Please respect Apple's terms of service.
Do not run this script too frequently to avoid overloading Apple's servers.
"""

def get_available_models(region=""):
    """
    從 Apple 商店頁面獲取當前可用的 iPhone 型號

    參數:
    region (str): 地區代碼，例如 "tw" 代表台灣，"" 代表美國

    返回:
    list: 可用的 iPhone 型號列表，例如 ["iphone-16-pro", "iphone-16", ...]
    """
    region_prefix = f"/{region}" if region else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-iphone"

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"無法訪問 {url}，使用預設型號列表")
            return ["iphone-16-pro", "iphone-16", "iphone-16e", "iphone-15"]

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 尋找所有指向 buy-iphone 頁面的連結
        iphone_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if '/shop/buy-iphone/iphone-' in href:
                # 提取型號部分 (例如從 /tw/shop/buy-iphone/iphone-16-pro 提取 iphone-16-pro)
                model = href.split('buy-iphone/')[1].split('?')[0].split('#')[0]
                iphone_links.append(model)

        # 去除重複項並返回
        unique_models = list(set(iphone_links))

        if not unique_models:
            print(f"在 {url} 找不到 iPhone 型號，使用預設型號列表")
            return ["iphone-16-pro", "iphone-16", "iphone-16e", "iphone-15"]

        return unique_models

    except Exception as e:
        print(f"獲取 iPhone 型號時出錯: {e}，使用預設型號列表")
        return ["iphone-16-pro", "iphone-16", "iphone-16e", "iphone-15"]

# 產品名稱標準化函數
def standardize_product_name(name):
    """標準化產品名稱，以便匹配相同的產品"""
    if not name:
        return ""

    # 移除空格，轉為小寫
    name = name.lower()

    # 提取型號部分 (如 "iPhone 16 Pro")
    model_match = re.search(r'iphone\s*(\d+)\s*(pro\s*max|pro|plus|se)?', name)

    # 提取容量部分 (如 "256GB")
    storage_match = re.search(r'(\d+)\s*(gb|tb)', name)

    # 提取顏色部分
    color_keywords = [
        "black", "white", "blue", "purple", "yellow", "green", 
        "pink", "red", "silver", "gold", "titanium", "starlight",
        "ultramarine", "teal", "desert", "natural", "gray", "graphite"
    ]

    found_color = None
    for color in color_keywords:
        if color in name:
            found_color = color
            break

    # 創建標準化鍵
    key_parts = []

    if model_match:
        model_num = model_match.group(1)
        model_variant = (model_match.group(2) or "").replace(" ", "")
        key_parts.append(f"iphone{model_num}{model_variant}")

    if storage_match:
        key_parts.append(f"{storage_match.group(1)}{storage_match.group(2)}")

    if found_color:
        key_parts.append(found_color)

    # 返回標準化鍵
    return "_".join(key_parts) if key_parts else name.replace(" ", "")

# Function to retrieve and extract product data from a page
def extract_product_details(url, is_taiwan=False):
    # Rate limiting - add a delay between requests to be respectful
    time.sleep(1)  # Sleep for 1 second between requests

    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for the script with type "application/json" and id "metrics"
    json_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
    if not json_script:
        print(f"No matching script found in {url}")
        return []

    # Parse JSON content
    json_data = json.loads(json_script.string)
    data = json_data.get('data', {})
    products = data.get('products', [])

    # Extract relevant product details
    product_details = []
    for product in products:
        sku = product.get("sku")
        name = product.get("name", "")
        price = product.get("price", {}).get("fullPrice")
        region = "TW" if is_taiwan else "US"

        # 生成標準化名稱以匹配產品
        std_name = standardize_product_name(name)

        product_details.append({
            "SKU": sku,
            "Name": name,
            "Price": price,
            "Region": region,
            "Standardized_Name": std_name
        })

    return product_details

# 動態獲取台灣和美國的 iPhone 型號
tw_models = get_available_models("tw")
us_models = get_available_models("")

# 合併兩個列表，確保所有型號都被包含
models = list(set(tw_models + us_models))

# Initialize an empty list to store product details from all URLs
all_product_details = []

# Loop through each model and add both English and Taiwan URL
for model in models:
    # 美國資料
    us_url = f"https://www.apple.com/shop/buy-iphone/{model}"
    us_products = extract_product_details(us_url, is_taiwan=False)
    all_product_details.extend(us_products)

    # 台灣資料
    tw_url = f"https://www.apple.com/tw/shop/buy-iphone/{model}"
    tw_products = extract_product_details(tw_url, is_taiwan=True)
    all_product_details.extend(tw_products)

# Convert the extracted data into a DataFrame
df = pd.DataFrame(all_product_details)

# 按地區分類數據
df_us = df[df['Region'] == 'US'].copy()
df_tw = df[df['Region'] == 'TW'].copy()

# 確保標準化名稱的唯一性
df_us = df_us.drop_duplicates(subset='Standardized_Name')
df_tw = df_tw.drop_duplicates(subset='Standardized_Name')

# 重命名列以便於合併後識別
df_us.rename(columns={'SKU': 'SKU_US', 'Price': 'Price_US', 'Name': 'Name_US'}, inplace=True)
df_tw.rename(columns={'SKU': 'SKU_TW', 'Price': 'Price_TW', 'Name': 'Name_TW'}, inplace=True)

# 使用標準化名稱進行合併
df_merged = pd.merge(df_us, df_tw, on='Standardized_Name', how='outer', suffixes=('_US', '_TW'))

# 為缺失值賦予預設值
df_merged['Price_US'] = df_merged['Price_US'].fillna(0)
df_merged['Price_TW'] = df_merged['Price_TW'].fillna(0)
df_merged['Name_US'] = df_merged['Name_US'].fillna('')
df_merged['Name_TW'] = df_merged['Name_TW'].fillna('')
df_merged['SKU_US'] = df_merged['SKU_US'].fillna('')
df_merged['SKU_TW'] = df_merged['SKU_TW'].fillna('')

# 選擇並重命名要保留的列
df_final = df_merged[['SKU_US', 'SKU_TW', 'Price_US', 'Price_TW', 'Name_US', 'Name_TW']].rename(
    columns={
        'Price_TW': '台灣價格',
        'Price_US': '美國價格',
        'Name_TW': '台灣產品名',
        'Name_US': '美國產品名'
    }
)

# 顯示最終結果
print(df_final)

# 保存結果到 CSV 文件
df_final.to_csv('iphone_products_merged.csv', index=False, encoding='utf-8-sig')