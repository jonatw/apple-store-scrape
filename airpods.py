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
    Get available AirPods models by analyzing the main AirPods marketing page
    
    Parameters:
    region_code (str): Region code, e.g., "tw" for Taiwan, "" for US
    
    Returns:
    list: List of available AirPods models
    """
    region_prefix = f"/{region_code}" if region_code else ""
    # Use the marketing page which has links to all models
    url = f"https://www.apple.com{region_prefix}/airpods/"
    
    # Default models as fallback
    default_models = ["airpods-4", "airpods-pro-2", "airpods-max"]
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Cannot access {url}, using default model list")
            return default_models

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all buy links for AirPods products
        airpods_models = []
        
        # Look for links containing /shop/goto/buy_airpods/
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            
            if '/shop/goto/buy_airpods/' in href:
                # Extract model from link (e.g. /us/shop/goto/buy_airpods/airpods_4)
                parts = href.split('buy_airpods/')
                if len(parts) > 1:
                    # Clean up query params or anchors
                    model_raw = parts[1].split('?')[0].split('#')[0]
                    
                    # Normalize model name: Apple often uses underscores in goto links (airpods_4) 
                    # but hyphens in store URLs (airpods-4).
                    model = model_raw.replace('_', '-')
                    
                    # Filter out sub-configurations (like /with_active_noise_cancellation) 
                    # We just want the base model name if possible, or we can try to scrape them all.
                    # If the model contains slashes, it might be a specific config. 
                    # Usually the first part is the model.
                    if '/' in model:
                        model = model.split('/')[0]
                        
                    if model and model != "": 
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
        
        product_details = []
        
        # Strategy 1: Try "metrics" script (standard for most pages)
        json_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
        if json_script:
            try:
                json_data = json.loads(json_script.string)
                data = json_data.get('data', {})
                products = data.get('products', [])
                
                if products:
                    debug_print(f"Found {len(products)} products via metrics for region {region_display}")
                    for product in products:
                        sku = product.get("sku")
                        name = product.get("name", "")
                        price = product.get("price", {}).get("fullPrice")
                        part_number = product.get("partNumber", "")
                        
                        # Derive BaseSKU
                        # If part_number has suffix like LL/A, strip it
                        base_sku = sku # Default to SKU
                        if part_number:
                             # Remove region suffix like /A, LL/A, TA/A
                             # Regex: Match 2 uppercase letters followed by / and 1 uppercase letter at end of string
                             base_sku = re.sub(r'[A-Z]{2}/[A-Z]$', '', part_number)
                             # Also handle simple /A case if any
                             base_sku = re.sub(r'/[A-Z]$', '', base_sku)

                        product_details.append({
                            "SKU": base_sku,
                            "OriginalSKU": sku or part_number,
                            "Name": name,
                            "Price": price,
                            "Region": region_display,
                            "Region_Code": region_code,
                            "PartNumber": part_number
                        })
                    return product_details
            except Exception as e:
                debug_print(f"Error parsing metrics JSON: {e}")

        # Strategy 2: Try "PRODUCT_SELECTION_BOOTSTRAP" (fallback for selection pages)
        debug_print("Metrics strategy failed or found no products, trying PRODUCT_SELECTION_BOOTSTRAP")
        
        # Find script containing the bootstrap variable
        script_content = None
        for script in soup.find_all('script'):
            if script.string and 'window.PRODUCT_SELECTION_BOOTSTRAP' in script.string:
                script_content = script.string
                break
        
        if script_content:
            try:
                # Locate productSelectionData
                key_index = script_content.find('productSelectionData:')
                if key_index != -1:
                    # Find start of the JSON object (first '{' after key)
                    start_index = script_content.find('{', key_index)
                    if start_index != -1:
                        # Extract JSON object by balancing braces
                        brace_count = 0
                        json_str = ""
                        for i in range(start_index, len(script_content)):
                            char = script_content[i]
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                            
                            json_str += char
                            
                            if brace_count == 0:
                                break
                        
                        if json_str:
                            bootstrap_data = json.loads(json_str)
                            
                            products = bootstrap_data.get('products', [])
                            display_values = bootstrap_data.get('displayValues', {})
                            prices_map = display_values.get('prices', {})
                            
                            if products:
                                 debug_print(f"Found {len(products)} products via bootstrap for region {region_display}")
                                 for product in products:
                                    part_number = product.get('partNumber')
                                    base_part_number = product.get('basePartNumber')
                                    
                                    # Try to find price info using 'fullPrice' OR 'price' key
                                    price_key = product.get('fullPrice')
                                    if not price_key:
                                        price_key = product.get('price')
                                        
                                    price_info = prices_map.get(price_key, {})
                                    
                                    # Extract numeric price
                                    price_val = None
                                    curr_price = price_info.get('currentPrice', {})
                                    if curr_price:
                                        raw_amount = curr_price.get('raw_amount')
                                        if raw_amount:
                                            try:
                                                price_val = float(raw_amount.replace(',', ''))
                                            except:
                                                pass
                                    
                                    # Name extraction
                                    name = product.get('familyType', '')
                                    # Heuristic: if name is all lowercase or matches internal ID pattern, try to find better name from page title
                                    if not name or name.islower() or name == 'airpodspro':
                                        page_title = soup.find('title')
                                        if page_title:
                                            # Title is usually "Product Name - Apple" or "Buy Product Name - Apple"
                                            # Clean up common suffixes/prefixes
                                            title_text = page_title.text.replace(' - Apple', '').strip()
                                            # Remove "Buy " only if it's at the start
                                            if title_text.startswith('Buy '):
                                                title_text = title_text[4:]
                                            
                                            if title_text:
                                                name = title_text.strip()
                                    
                                    if not name:
                                        name = "Unknown Product"
                                    
                                    # Use basePartNumber as SKU for merging if available
                                    base_sku = base_part_number if base_part_number else part_number
                                    
                                    product_details.append({
                                        "SKU": base_sku,
                                        "OriginalSKU": part_number,
                                        "Name": name,
                                        "Price": price_val,
                                        "Region": region_display,
                                        "Region_Code": region_code,
                                        "PartNumber": part_number
                                    })
                                 return product_details
            except Exception as e:
                debug_print(f"Error parsing bootstrap JSON: {e}")

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
    # Get all unique models from all regions
    all_models = set()
    for region_code in REGIONS.keys():
        models = get_available_models(region_code)
        all_models.update(models)
    
    debug_print(f"Found models across all regions: {', '.join(all_models)}")
    
    # Fetch products for each model from each region using correct URL pattern
    all_products = []
    for model in all_models:
        for region_code in REGIONS.keys():
            region_prefix = f"/{region_code}" if region_code else ""
            # Use the correct final URL pattern
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

def consolidate_similar_colors(df, price_tolerance=0.02):
    """
    Consolidate AirPods products with same specs but different colors when prices are similar
    Removes color information completely for clean model-only output
    """
    if df.empty:
        return df
    
    # Find the product name column (could be different naming)
    product_name_col = None
    for col in df.columns:
        if 'Name_' in col or col == 'PRODUCT_NAME':
            product_name_col = col
            break
    
    if not product_name_col:
        debug_print("No product name column found, skipping consolidation")
        return df
    
    # AirPods-specific color patterns
    color_patterns = [
        r'\b(space\s+gray|rose\s+gold|sky\s+blue|pink|blue|green|midnight|starlight)\b',
        r'\b(black|white|silver|gold|gray|grey|red|purple|orange)\b',
        r'\b(natural|graphite|jet\s+black|product\s+red)\b'
    ]
    
    def extract_base_name_and_colors(product_name):
        """Extract base model name and colors separately"""
        if not product_name:
            return product_name, []
        
        name_lower = product_name.lower()
        found_colors = []
        
        # Extract colors (longest patterns first)
        for pattern in color_patterns:
            matches = re.findall(pattern, name_lower, re.IGNORECASE)
            found_colors.extend([m.strip().title() if isinstance(m, str) else ' '.join(m).strip().title() for m in matches])
            # Remove found colors from name
            name_lower = re.sub(pattern, ' ', name_lower, flags=re.IGNORECASE)
        
        # Clean up base name
        base_name = re.sub(r'\s+', ' ', name_lower).strip().title()
        return base_name, list(set(found_colors))
    
    # Add base name and color extraction
    df_copy = df.copy()
    df_copy['Base_Name'] = ''
    df_copy['Colors'] = None  # Use None instead of empty string for lists
    
    base_names = []
    colors_list = []
    
    for idx, row in df_copy.iterrows():
        base_name, colors = extract_base_name_and_colors(row[product_name_col])
        base_names.append(base_name)
        colors_list.append(colors)
    
    df_copy['Base_Name'] = base_names
    df_copy['Colors'] = colors_list
    
    # Group by base name and check if consolidation is appropriate
    consolidated_rows = []
    
    for base_name, group in df_copy.groupby('Base_Name'):
        if len(group) <= 1:
            # Single variant, keep as is
            for _, row in group.iterrows():
                consolidated_rows.append(row)
        else:
            # Multiple variants - check if prices are similar
            price_cols = [col for col in group.columns if col.startswith('Price_')]
            
            should_consolidate = True
            for price_col in price_cols:
                prices = group[price_col].dropna()
                if len(prices) > 1:
                    price_range = max(prices) - min(prices)
                    avg_price = sum(prices) / len(prices)
                    if avg_price > 0 and price_range / avg_price > price_tolerance:
                        should_consolidate = False
                        break
            
            if should_consolidate and len(group) > 1:
                # Consolidate: use first row as template, update name
                consolidated = group.iloc[0].copy()
                consolidated[product_name_col] = base_name
                debug_print(f"Consolidated {len(group)} color variants into single entry: '{base_name}'")
                consolidated_rows.append(consolidated)
            else:
                # Don't consolidate - keep separate (prices differ significantly)
                for _, row in group.iterrows():
                    consolidated_rows.append(row)
    
    # Create result DataFrame
    result_df = pd.DataFrame(consolidated_rows)
    
    # Remove helper columns
    result_df = result_df.drop(['Base_Name', 'Colors'], axis=1, errors='ignore')
    
    return result_df

def main():
    """Main execution function"""
    print("Starting AirPods product scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    
    # Get all products from all regions
    all_products = get_all_products()
    
    # Merge product data
    merged_data = merge_product_data(all_products)
    
    # Apply color consolidation (remove color information)
    merged_data = consolidate_similar_colors(merged_data)
    
    # Display results
    print("\nResults:")
    print(merged_data)
    
    # Save consolidated results to CSV
    output_file = 'airpods_products_merged.csv'
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved consolidated results to {output_file}")
    
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