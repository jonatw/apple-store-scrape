import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

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

def get_available_models(region_code=""):
    """
    Get available iPad models from Apple store page
    
    Parameters:
    region_code (str): Region code, e.g., "tw" for Taiwan, "" for US
    
    Returns:
    list: List of available iPad models, e.g., ["ipad-pro", "ipad-air", ...]
    """
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-ipad"
    
    default_models = ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Cannot access {url}, using default model list")
            return default_models

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links to buy-ipad pages
        ipad_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if '/shop/buy-ipad/' in href:
                # Extract model part (e.g., extract ipad-pro from /tw/shop/buy-ipad/ipad-pro)
                parts = href.split('/shop/buy-ipad/')
                if len(parts) > 1:
                    model = parts[1].split('?')[0].split('#')[0]
                    # Ensure it's a valid iPad model
                    if model.startswith('ipad-') or model == 'ipad':
                        ipad_links.append(model)

        # Remove duplicates and return
        unique_models = list(set(ipad_links))

        if not unique_models:
            debug_print(f"Could not find iPad models at {url}, using default model list")
            return default_models

        return unique_models

    except Exception as e:
        debug_print(f"Error getting iPad models: {e}, using default model list")
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
            
            product_details.append({
                "SKU": sku,
                "Name": name,
                "Price": price,
                "Region": region_display,
                "Region_Code": region_code,
                "PartNumber": part_number
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
            url = f"https://www.apple.com{region_prefix}/shop/buy-ipad/{model}"
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
        
        # Ensure uniqueness of SKUs
        region_data = region_data.drop_duplicates(subset='SKU')
        
        # Rename columns to include region
        region_data.rename(columns={
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
    
    # Get the base dataframe
    merged_df = region_dfs[ref_region][['SKU', f'Price_{ref_display}', f'Name_{ref_display}']].copy()
    
    # Merge with other regions using SKU as the key
    for region_code, region_df in region_dfs.items():
        if region_code == ref_region:
            continue
        
        region_display = REGIONS[region_code][0]
        
        # Select columns to merge
        columns_to_merge = ['SKU', f'Price_{region_display}', f'Name_{region_display}']
            
        merged_df = pd.merge(
            merged_df, 
            region_df[columns_to_merge], 
            on='SKU', 
            how='outer'
        )
    
    # Fill missing values
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        merged_df[f'Price_{region_display}'] = merged_df[f'Price_{region_display}'].fillna(0)
        merged_df[f'Name_{region_display}'] = merged_df[f'Name_{region_display}'].fillna('')
    
    # Create final output dataframe with columns in the desired order:
    # 1. SKU (common for all regions, so no need for region prefix)
    # 2. Price columns for each region 
    # 3. Product name from reference region
    
    # Prepare the price columns
    price_columns = []
    
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        price_columns.append(f'Price_{region_display}')
    
    # Create the output dataframe with columns in the specified order
    output_columns = ['SKU'] + price_columns + [f'Name_{ref_display}']
    output_df = merged_df[output_columns].copy()
    
    # Rename the product name column
    output_df = output_df.rename(columns={f'Name_{ref_display}': 'PRODUCT_NAME'})
    
    return output_df

# ==================== MAIN EXECUTION ====================

def main():
    """Main execution function"""
    print("Starting iPad product scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    
    # Get all products from all regions
    all_products = get_all_products()
    
    # Merge product data
    merged_data = merge_product_data(all_products)
    
    # Display results
    print("\nResults:")
    print(merged_data)
    
    # Save to CSV
    output_file = 'ipad_products_merged.csv'
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