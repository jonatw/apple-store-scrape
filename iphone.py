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

# ==================== CONFIGURATION ====================

# Define regions to scrape
# Format: region_code: [display_name, currency_code, locale, currency_symbol]
# Use empty string "" for US as it has no region prefix in URL
REGIONS = {
    "": ["US", "USD", "en-us", "$"],       # United States
    "tw": ["TW", "TWD", "zh-tw", "NT$"],   # Taiwan
    # Uncomment or add more regions as needed:
    # "jp": ["JP", "JPY", "ja-jp", "¥"],      # Japan
    # "uk": ["UK", "GBP", "en-gb", "£"],      # United Kingdom
    # "au": ["AU", "AUD", "en-au", "A$"],     # Australia
    # "ca": ["CA", "CAD", "en-ca", "C$"],     # Canada
    # "de": ["DE", "EUR", "de-de", "€"],      # Germany
    # "fr": ["FR", "EUR", "fr-fr", "€"],      # France
}

# Reference region for product naming (first one will be used as reference)
REFERENCE_REGION = list(REGIONS.keys())[0]

# Request delay to avoid overloading servers (seconds)
REQUEST_DELAY = 1

# Set to True to print debug information
DEBUG = True

# ==================== FUNCTIONS ====================

def debug_print(message):
    """Print debug message if DEBUG is enabled"""
    if DEBUG:
        print(f"[DEBUG] {message}")

def standardize_product_name(name):
    """
    Standardize product name for matching across regions
    
    Parameters:
    name (str): Original product name, e.g., "iPhone 16 Pro 256GB Black Titanium"
    
    Returns:
    str: Standardized name key, e.g., "iphone16pro_256gb_blacktitanium"
    """
    if not name:
        return ""

    # Convert to lowercase
    name = name.lower()

    # Extract model part
    model_match = re.search(r'iphone\s*(\d+)\s*(pro\s*max|pro|plus|se)?', name)

    # Extract capacity part
    storage_match = re.search(r'(\d+)\s*(gb|tb)', name)

    # Extract color by removing model and capacity parts
    name_copy = name
    if model_match:
        name_copy = name_copy.replace(model_match.group(0), "")
    if storage_match:
        name_copy = name_copy.replace(storage_match.group(0), "")
    
    # Clean up the remaining text to get the color
    color = name_copy.strip().replace(" ", "")
    
    # Create standardized key parts
    key_parts = []

    if model_match:
        model_num = model_match.group(1)
        model_variant = (model_match.group(2) or "").replace(" ", "")
        key_parts.append(f"iphone{model_num}{model_variant}")

    if storage_match:
        key_parts.append(f"{storage_match.group(1)}{storage_match.group(2)}")

    if color:
        key_parts.append(color)

    # Join key parts with underscore
    return "_".join(key_parts) if key_parts else name.replace(" ", "")

def get_available_models(region_code=""):
    """
    Get available iPhone models from Apple store page
    
    Parameters:
    region_code (str): Region code, e.g., "tw" for Taiwan, "" for US
    
    Returns:
    list: List of available iPhone models, e.g., ["iphone-16-pro", "iphone-16", ...]
    """
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-iphone"
    
    default_models = ["iphone-16-pro", "iphone-16", "iphone-16e", "iphone-15"]
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Cannot access {url}, using default model list")
            return default_models

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links to buy-iphone pages
        iphone_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if '/shop/buy-iphone/iphone-' in href:
                # Extract model part (e.g., extract iphone-16-pro from /tw/shop/buy-iphone/iphone-16-pro)
                model = href.split('buy-iphone/')[1].split('?')[0].split('#')[0]
                iphone_links.append(model)

        # Remove duplicates and return
        unique_models = list(set(iphone_links))

        if not unique_models:
            debug_print(f"Could not find iPhone models at {url}, using default model list")
            return default_models

        return unique_models

    except Exception as e:
        debug_print(f"Error getting iPhone models: {e}, using default model list")
        return default_models

def extract_product_details(url, region_code=""):
    """
    Extract product details from Apple store page
    
    Parameters:
    url (str): URL of the Apple store product page
    region_code (str): Region code to identify the region
    
    Returns:
    list: List of dictionaries containing product details
    """
    # Rate limiting
    time.sleep(REQUEST_DELAY)
    
    # Get region display name
    region_display = REGIONS.get(region_code, ["Unknown"])[0]
    
    debug_print(f"Fetching products from {url} for region {region_display}")
    
    response = requests.get(url)

    if response.status_code != 200:
        debug_print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Search for the script with type "application/json" and id "metrics"
    json_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
    if not json_script:
        debug_print(f"No matching script found in {url}")
        return []

    # Parse JSON content
    try:
        json_data = json.loads(json_script.string)
        data = json_data.get('data', {})
        products = data.get('products', [])
        
        # Debug info
        debug_print(f"Found {len(products)} products for region {region_display}")
        
        # Extract relevant product details
        product_details = []
        for product in products:
            sku = product.get("sku")
            name = product.get("name", "")
            price = product.get("price", {}).get("fullPrice")
            part_number = product.get("partNumber", "")
            
            # Generate standardized name for matching products across regions
            std_name = standardize_product_name(name)
            
            product_details.append({
                "SKU": sku,
                "Name": name,
                "Price": price,
                "Region": region_display,
                "Region_Code": region_code,
                "PartNumber": part_number,
                "Standardized_Name": std_name
            })
            
        return product_details
    except Exception as e:
        debug_print(f"Error parsing product data: {e}")
        return []

def get_all_products():
    """
    Get all products from all configured regions
    
    Returns:
    list: Combined list of all product details from all regions
    """
    # Get all unique models from all regions
    all_models = set()
    for region_code in REGIONS.keys():
        models = get_available_models(region_code)
        all_models.update(models)
    
    debug_print(f"Found models across all regions: {', '.join(all_models)}")
    
    # Fetch products for each model from each region
    all_products = []
    for model in all_models:
        for region_code in REGIONS.keys():
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/shop/buy-iphone/{model}"
            products = extract_product_details(url, region_code)
            all_products.extend(products)
    
    return all_products

def merge_product_data(product_data):
    """
    Merge product data from all regions
    
    Parameters:
    product_data (list): List of product dictionaries
    
    Returns:
    DataFrame: Merged product data with columns for each region
    """
    # Convert to DataFrame
    df = pd.DataFrame(product_data)
    
    if df.empty:
        debug_print("No product data to merge!")
        return pd.DataFrame()
    
    # Create separate DataFrames for each region
    region_dfs = {}
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        region_data = df[df['Region_Code'] == region_code].copy()
        
        # Ensure uniqueness of standardized names
        region_data = region_data.drop_duplicates(subset='Standardized_Name')
        
        # Rename columns to include region
        region_data.rename(columns={
            'SKU': f'SKU_{region_display}',
            'Price': f'Price_{region_display}',
            'Name': f'Name_{region_display}',
            'PartNumber': f'PartNumber_{region_display}'
        }, inplace=True)
        
        # Store for merging
        region_dfs[region_code] = region_data
    
    # Start with the reference region
    ref_region = REFERENCE_REGION
    ref_display = REGIONS[ref_region][0]
    
    if ref_region not in region_dfs:
        debug_print(f"Reference region {ref_display} not found in data!")
        return pd.DataFrame()
    
    merged_df = region_dfs[ref_region]
    
    # Merge with other regions
    for region_code, region_df in region_dfs.items():
        if region_code == ref_region:
            continue
        
        # Select columns to merge
        columns_to_merge = [
            f'SKU_{REGIONS[region_code][0]}', 
            f'Price_{REGIONS[region_code][0]}', 
            'Standardized_Name'
        ]
            
        merged_df = pd.merge(
            merged_df, 
            region_df[columns_to_merge], 
            on='Standardized_Name', 
            how='outer'
        )
    
    # Fill NaN values
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        merged_df[f'Price_{region_display}'] = merged_df[f'Price_{region_display}'].fillna(0)
        merged_df[f'SKU_{region_display}'] = merged_df[f'SKU_{region_display}'].fillna('')
    
    # Create final output dataframe with the requested column format
    # 1. First all SKU columns
    # 2. Then all Price columns
    # 3. Finally the product name
    
    # Prepare the output columns in the desired order
    sku_columns = []
    price_columns = []
    
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        sku_columns.append(f'SKU_{region_display}')
        price_columns.append(f'Price_{region_display}')
    
    # Create the output dataframe with columns in the specified order
    output_columns = sku_columns + price_columns + [f'Name_{ref_display}']
    output_df = merged_df[output_columns].copy()
    
    # Rename the product name column
    output_df = output_df.rename(columns={f'Name_{ref_display}': 'PRODUCT_NAME'})
    
    return output_df

# ==================== MAIN EXECUTION ====================

def main():
    """Main execution function"""
    print("Starting iPhone product scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    
    # Get all products from all regions
    all_products = get_all_products()
    
    # Merge product data
    merged_data = merge_product_data(all_products)
    
    # Display results
    print("\nResults:")
    print(merged_data)
    
    # Save to CSV
    output_file = 'iphone_products_merged.csv'
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved results to {output_file}")
    
    # Display stats
    print(f"\nTotal unique products found: {len(merged_data)}")
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        price_col = f'Price_{region_display}'
        
        if price_col in merged_data.columns:
            non_zero_prices = (merged_data[price_col] > 0).sum()
            print(f"Products found in {region_display}: {non_zero_prices}")

if __name__ == "__main__":
    main()