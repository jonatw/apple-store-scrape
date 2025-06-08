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

def standardize_product_name(name):
    """
    Standardize product name for matching across regions
    
    Parameters:
    name (str): Original product name
    
    Returns:
    str: Standardized name key for matching
    """
    if not name:
        return ""
    
    # Convert to lowercase and replace spaces/commas with underscores
    name = name.lower()
    name = name.replace(" ", "_").replace(",", "")
    
    # Remove common words that might vary
    name = name.replace("apple_watch_", "")
    name = name.replace("series_10", "s10")
    
    return name

def get_available_models(region_code=""):
    """
    Get available Apple Watch models from Apple store page
    
    Parameters:
    region_code (str): Region code, e.g., "tw" for Taiwan, "" for US
    
    Returns:
    list: List of available Apple Watch models, e.g., ["apple-watch", "apple-watch-se", ...]
    """
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-watch"
    
    default_models = ["apple-watch", "apple-watch-se", "apple-watch-ultra", "apple-watch-hermes"]
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Cannot access {url}, using default model list")
            return default_models

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links to buy-watch pages
        watch_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if '/shop/buy-watch/' in href:
                # Extract model part (e.g., extract apple-watch from /tw/shop/buy-watch/apple-watch)
                parts = href.split('/shop/buy-watch/')
                if len(parts) > 1:
                    model = parts[1].split('?')[0].split('#')[0].split('/')[0]
                    # Ensure it's a valid Watch model
                    if model.startswith('apple-watch') or model == 'apple-watch':
                        watch_links.append(model)

        # Remove duplicates and return
        unique_models = list(set(watch_links))

        if not unique_models:
            debug_print(f"Could not find Apple Watch models at {url}, using default model list")
            return default_models

        debug_print(f"Found models: {', '.join(unique_models)}")
        return unique_models

    except Exception as e:
        debug_print(f"Error getting Apple Watch models: {e}, using default model list")
        return default_models

def extract_product_details(url, region_code=""):
    """
    Extract product details from Apple Watch store page (different structure than iPhone/iPad)
    
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
        
        # Apple Watch pages use a different structure - look for PRODUCT_SELECTION_BOOTSTRAP
        product_selection_script = None
        for script in soup.find_all('script'):
            if script.string and 'PRODUCT_SELECTION_BOOTSTRAP' in script.string:
                product_selection_script = script
                break
        
        if not product_selection_script:
            debug_print(f"No PRODUCT_SELECTION_BOOTSTRAP script found in {url}")
            return []
        
        # Extract the JSON data from the script
        script_content = product_selection_script.string
        start_marker = 'productSelectionData: '
        start_idx = script_content.find(start_marker)
        if start_idx == -1:
            debug_print(f"No productSelectionData found in script for {url}")
            return []
        
        start_idx += len(start_marker)
        
        # Find the end of the JSON object
        brace_count = 0
        end_idx = start_idx
        in_string = False
        escape_next = False
        
        for i, char in enumerate(script_content[start_idx:]):
            actual_idx = start_idx + i
            
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
                
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = actual_idx + 1
                        break
        
        json_str = script_content[start_idx:end_idx]
        
        try:
            product_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            debug_print(f"Failed to parse product selection JSON for {url}: {e}")
            return []
        
        # Extract products and prices
        products = product_data.get('products', [])
        prices = product_data.get('displayValues', {}).get('prices', {})
        
        debug_print(f"Found {len(products)} products for region {region_display}")
        
        # Extract relevant product details
        product_details = []
        for product in products:
            part_number = product.get("part", "")
            price_key = product.get("priceKey", "")
            dimensions = product.get("dimensions", {})
            
            # Get price from prices dictionary
            price_info = prices.get(price_key, {})
            price = price_info.get("amount", 0)
            
            # Build product name from dimensions and URL info
            case_size = dimensions.get("watch_cases-dimensionCaseSize", "")
            case_material = dimensions.get("watch_cases-dimensionCaseMaterial", "")
            case_color = dimensions.get("watch_cases-dimensionColor", "")
            connectivity = dimensions.get("watch_cases-dimensionConnection", "")
            
            # Format connectivity
            conn_formatted = ""
            if connectivity == "gps":
                conn_formatted = "GPS"
            elif connectivity == "gpscell":
                conn_formatted = "GPS + Cellular"
            
            # Determine watch model from URL
            watch_model = "Apple Watch Series 10"
            if "apple-watch-se" in url:
                watch_model = "Apple Watch SE"
            elif "apple-watch-ultra" in url:
                watch_model = "Apple Watch Ultra 2"
            elif "apple-watch-hermes" in url:
                if "ultra" in url:
                    watch_model = "Apple Watch Hermès Ultra 2"
                else:
                    watch_model = "Apple Watch Hermès Series 10"
            
            # Build product name
            name_parts = [watch_model]
            if conn_formatted:
                name_parts.append(conn_formatted)
            if case_size:
                name_parts.append(case_size)
            if case_color and case_material:
                # Format color name (replace underscores, capitalize)
                color_formatted = case_color.replace("_", " ").title()
                material_formatted = case_material.title()
                name_parts.append(f"{color_formatted} {material_formatted}")
            
            name = ", ".join(name_parts)
            
            # Use part number as SKU for consistency
            sku = part_number
            
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
        debug_print(f"Error extracting products from {url}: {e}")
        return []

def get_all_products():
    """
    Get all Apple Watch products from all regions
    
    Returns:
    list: List of all products from all regions
    """
    # Get all unique models from all regions (same approach as working scrapers)
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
            url = f"https://www.apple.com{region_prefix}/shop/buy-watch/{model}"
            products = extract_product_details(url, region_code)
            all_products.extend(products)
    
    return all_products

def merge_product_data(product_data):
    """
    Merge product data from all regions using standardized name matching (same as iPhone scraper)
    
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
    
    # Merge with other regions using standardized name as the key
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

def main():
    """Main execution function"""
    print("Starting Apple Watch product scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    
    # Get all products from all regions
    all_products = get_all_products()
    
    # Merge product data
    merged_data = merge_product_data(all_products)
    
    # Display results
    print("\nResults:")
    print(merged_data)
    
    # Save to CSV
    output_file = 'watch_products_merged.csv'
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved results to {output_file}")
    
    # Display stats
    print(f"\nTotal unique products found: {len(merged_data)}")
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        price_col = f'Price_{region_display}'
        sku_col = f'SKU_{region_display}'
        
        if price_col in merged_data.columns:
            non_zero_prices = (merged_data[price_col] > 0).sum()
            print(f"Products found in {region_display}: {non_zero_prices}")

if __name__ == "__main__":
    main()