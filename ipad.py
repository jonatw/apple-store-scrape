import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time  # Added for rate limiting

# Disclaimer
"""
This tool is for personal research and comparison only. Please respect Apple's terms of service.
Do not run this script too frequently to avoid overloading Apple's servers.
"""

# Define the base URL for the iPad product pages
base_url = "https://www.apple.com/shop/buy-ipad"

def get_available_models(region=""):
    """
    從 Apple 商店頁面獲取當前可用的 iPad 型號
    
    參數:
    region (str): 地區代碼，例如 "tw" 代表台灣，"" 代表美國
    
    返回:
    list: 可用的 iPad 型號列表，例如 ["ipad-pro", "ipad-air", ...]
    """
    region_prefix = f"/{region}" if region else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-ipad"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"無法訪問 {url}，使用預設型號列表")
            return ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]
        
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 尋找所有指向 buy-ipad 頁面的連結
        ipad_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if '/shop/buy-ipad/' in href:
                # 提取型號部分 (例如從 /tw/shop/buy-ipad/ipad-pro 提取 ipad-pro)
                parts = href.split('/shop/buy-ipad/')
                if len(parts) > 1:
                    model = parts[1].split('?')[0].split('#')[0]
                    # 確保獲取的是有效的 iPad 型號
                    if model.startswith('ipad-') or model == 'ipad':
                        ipad_links.append(model)
        
        # 去除重複項並返回
        unique_models = list(set(ipad_links))
        
        if not unique_models:
            print(f"在 {url} 找不到 iPad 型號，使用預設型號列表")
            return ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]
        
        return unique_models
    
    except Exception as e:
        print(f"獲取 iPad 型號時出錯: {e}，使用預設型號列表")
        return ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]

# 動態獲取台灣和美國的 iPhone 型號
tw_models = get_available_models("tw")
us_models = get_available_models("")

# 合併兩個列表，確保所有型號都被包含
models = list(set(tw_models + us_models))

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
        name_en = product.get("name", "")
        name_zh = name_en if is_taiwan else ""
        price = product.get("price", {}).get("fullPrice")
        category = product.get("category")
        part_number = product.get("partNumber")
        
        # Add English and Chinese names as separate columns
        if is_taiwan:
            name_zh = product.get("name", "")
            name_en = ""  # Empty for Taiwan
        product_details.append({
            "SKU": sku,
            "Part Number": part_number,
            "Price (USD)": price if not is_taiwan else None,  # Use None instead of empty string
            "Price (TWD)": price if is_taiwan else None,      # Use None instead of empty string
            "Category": category,
            "Name (English)": name_en,
            "Name (Chinese)": name_zh
        })
    return product_details

# Initialize an empty list to store product details from all URLs
all_product_details = []

# Loop through each model and add both English and Taiwan URL
for model in models:
    for region in ["", "tw"]:  # "" for US and "tw" for Taiwan
        if region:
            url = f"https://www.apple.com/{region}/shop/buy-ipad/{model}"
        else:
            url = f"https://www.apple.com/shop/buy-ipad/{model}"
        is_taiwan = region == "tw"
        product_details = extract_product_details(url, is_taiwan)
        all_product_details.extend(product_details)

# Convert the extracted data into a DataFrame
df_product_details = pd.DataFrame(all_product_details)

# Separate US and Taiwan data based on non-null price fields
df_us = df_product_details[['SKU', 'Price (USD)', 'Name (English)']].dropna(subset=['Price (USD)'])
df_tw = df_product_details[['SKU', 'Price (TWD)', 'Name (Chinese)']].dropna(subset=['Price (TWD)'])

# Ensure SKU uniqueness by dropping duplicates
df_us = df_us.drop_duplicates(subset='SKU')
df_tw = df_tw.drop_duplicates(subset='SKU')

# Merge US and Taiwan data on SKU
df_merged = pd.merge(df_us, df_tw, on='SKU', how='outer')

# Fill missing values appropriately
df_merged['Price (USD)'] = df_merged['Price (USD)'].fillna(0)
df_merged['Price (TWD)'] = df_merged['Price (TWD)'].fillna(0)
df_merged['Name (English)'] = df_merged['Name (English)'].fillna('')
df_merged['Name (Chinese)'] = df_merged['Name (Chinese)'].fillna('')

# Rename columns to match desired output
df_final = df_merged.rename(columns={
    "Price (TWD)": "台灣價格",
    "Price (USD)": "美國價格",
    "Name (Chinese)": "台灣產品名",
    "Name (English)": "美國產品名"
})[["SKU", "台灣價格", "美國價格", "台灣產品名", "美國產品名"]]

# Display the final DataFrame
print(df_final)

# Optional: Save the final DataFrame to a CSV file
df_final.to_csv('ipad_products_merged.csv', index=False, encoding='utf-8-sig')
