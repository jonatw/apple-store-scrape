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
REGIONS = {
    "": ["US", "USD", "en-us", "$"],       # United States
    "tw": ["TW", "TWD", "zh-tw", "NT$"],   # Taiwan
}

# Reference region for product naming
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
    Get available AirPods models by analyzing the main AirPods page
    
    Parameters:
    region_code (str): Region code, e.g., "tw" for Taiwan, "" for US
    
    Returns:
    list: List of available AirPods models
    """
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/airpods"
    
    # Updated default models based on current Apple lineup
    default_models = ["airpods_4", "airpods_pro_2", "airpods_max"]
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Cannot access {url}, using default model list")
            return default_models

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all buy links for AirPods products (using correct URL pattern)
        airpods_models = []
        
        # Look for buy/goto patterns
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            
            # Check for buy/goto patterns (correct Apple URL structure)
            if '/shop/goto/buy_airpods/' in href:
                # Extract model from buy link
                model = href.split('buy_airpods/')[1].split('?')[0].split('#')[0]
                airpods_models.append(model)

        # Remove duplicates and clean up
        unique_models = list(set(airpods_models))

        if not unique_models:
            debug_print(f"Could not find AirPods models at {url}, using default model list")
            return default_models

        debug_print(f"Found models: {', '.join(unique_models)}")
        return unique_models

    except Exception as e:
        debug_print(f"Error getting AirPods models: {e}, using default model list")
        return default_models

# Remove this function as it's not needed - we'll use the correct URL pattern instead

def extract_product_details(url, region_code=""):
    """
    Extract product details from Apple store page using the same method as working scrapers
    
    Parameters:
    url (str): Product page URL
    region_code (str): Region code
    
    Returns:
    list: List of product details
    """
    # Rate limiting
    time.sleep(REQUEST_DELAY)
    
    # Get region display name
    region_display = REGIONS.get(region_code, ["Unknown"])[0]
    
    debug_print(f"Fetching products from {url} for region {region_display}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return []
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Search for the script with type "application/json" and id "metrics" (same as working scrapers)
        json_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
        if not json_script:
            debug_print(f"No matching script found in {url}")
            return []
        
        # Parse JSON content
        json_data = json.loads(json_script.string)
        data = json_data.get('data', {})
        products = data.get('products', [])
        
        debug_print(f"Found {len(products)} products for region {region_display}")
        
        # Extract relevant product details (same format as iPhone/iPad scrapers)
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
        debug_print(f"Error extracting products from {url}: {e}")
        return []

def get_all_products():
    """
    Get all AirPods products from all regions
    
    Returns:
    list: List of all products from all regions
    """
    # Use known working AirPods models with correct URL format (hyphens, not underscores)
    known_models = ["airpods-4", "airpods-pro", "airpods-max"]
    
    debug_print(f"Using known AirPods models: {', '.join(known_models)}")
    
    # Fetch products for each model from each region using correct URL pattern
    all_products = []
    for model in known_models:
        for region_code in REGIONS.keys():
            region_prefix = f"/{region_code}" if region_code else ""
            # Use the correct final URL pattern (not goto redirect)
            url = f"https://www.apple.com{region_prefix}/shop/buy-airpods/{model}"
            products = extract_product_details(url, region_code)
            all_products.extend(products)
    
    return all_products

def merge_product_data(product_data):
    """
    Merge product data from all regions using SKU-based matching (same as iPad scraper)
    
    Parameters:
    product_data (list): List of product data from all regions
    
    Returns:
    pandas.DataFrame: Merged product data
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

def main():
    """Main execution function"""
    print("Starting AirPods product scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    
    # Get all products from all regions
    all_products = get_all_products()
    
    # Merge product data
    merged_data = merge_product_data(all_products)
    
    # Display results
    print("\nResults:")
    print(merged_data)
    
    # Save to CSV
    output_file = 'airpods_products_merged.csv'
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