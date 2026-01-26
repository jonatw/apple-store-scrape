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
    Get available Apple TV and Home products by analyzing the main TV/Home pages
    """
    region_prefix = f"/{region_code}" if region_code else ""
    
    # URLs to check for TV and Home products
    tv_url = f"https://www.apple.com{region_prefix}/tv-home/"
    
    # Default models based on current Apple lineup
    default_models = {
        'tv': ['apple-tv-4k'],
        'homepod': ['homepod', 'homepod-mini']
    }
    
    found_models = {'tv': [], 'homepod': []}
    
    # Check TV/Home landing page
    try:
        response = requests.get(tv_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                
                # Check for buy links
                if '/shop/goto/buy_tv/' in href:
                    parts = href.split('buy_tv/')
                    if len(parts) > 1:
                        model_raw = parts[1].split('?')[0].split('#')[0]
                        model = model_raw.replace('_', '-')
                        if model: found_models['tv'].append(model)
                
                elif '/shop/goto/buy_homepod/' in href:
                    parts = href.split('buy_homepod/')
                    if len(parts) > 1:
                        model_raw = parts[1].split('?')[0].split('#')[0]
                        model = model_raw.replace('_', '-')
                        if model: found_models['homepod'].append(model)
                    
    except Exception as e:
        debug_print(f"Error accessing {tv_url}: {e}")
    
    # Clean up and fallback
    for category in found_models:
        found_models[category] = list(set(found_models[category]))
        if not found_models[category]:
            found_models[category] = default_models[category]
    
    debug_print(f"Found TV models: {', '.join(found_models['tv'])}")
    debug_print(f"Found HomePod models: {', '.join(found_models['homepod'])}")
    
    return found_models

def extract_product_details(url, region_code=""):
    """
    Extract product details from Apple store page using robust dual-strategy
    """
    time.sleep(REQUEST_DELAY)
    region_display = REGIONS.get(region_code, ["Unknown"])[0]
    debug_print(f"Fetching products from {url} for region {region_display}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        product_details = []
        
        # Strategy 1: Metrics JSON
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
                        
                        base_sku = sku
                        if part_number:
                             base_sku = re.sub(r'[A-Z]{2}/[A-Z]$', '', part_number)
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

        # Strategy 2: PRODUCT_SELECTION_BOOTSTRAP
        debug_print("Metrics strategy failed or found no products, trying PRODUCT_SELECTION_BOOTSTRAP")
        
        script_content = None
        for script in soup.find_all('script'):
            if script.string and 'window.PRODUCT_SELECTION_BOOTSTRAP' in script.string:
                script_content = script.string
                break
        
        if script_content:
            try:
                key_index = script_content.find('productSelectionData:')
                if key_index != -1:
                    start_index = script_content.find('{', key_index)
                    if start_index != -1:
                        brace_count = 0
                        json_str = ""
                        for i in range(start_index, len(script_content)):
                            char = script_content[i]
                            if char == '{': brace_count += 1
                            elif char == '}': brace_count -= 1
                            json_str += char
                            if brace_count == 0: break
                        
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
                                    
                                    price_key = product.get('fullPrice') or product.get('price')
                                    price_info = prices_map.get(price_key, {})
                                    
                                    price_val = None
                                    curr_price = price_info.get('currentPrice', {})
                                    if curr_price:
                                        raw_amount = curr_price.get('raw_amount')
                                        if raw_amount:
                                            try:
                                                price_val = float(raw_amount.replace(',', ''))
                                            except:
                                                pass
                                    
                                    name = product.get('familyType', '')
                                    if not name:
                                        name = soup.find('title').text.split('-')[0].strip() if soup.find('title') else "Unknown Product"
                                    
                                    base_sku = base_part_number
                                    if not base_sku and part_number:
                                         base_sku = re.sub(r'[A-Z]{2}/[A-Z]$', '', part_number)
                                         base_sku = re.sub(r'/[A-Z]$', '', base_sku)
                                    
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
    Get all Apple TV and Home products from all regions
    """
    models_dict = {'tv': set(), 'homepod': set()}
    for region_code in REGIONS.keys():
        found = get_available_models(region_code)
        models_dict['tv'].update(found['tv'])
        models_dict['homepod'].update(found['homepod'])
    
    all_products = []
    
    # Process TV products
    for model in models_dict['tv']:
        for region_code in REGIONS.keys():
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/shop/buy-tv/{model}"
            products = extract_product_details(url, region_code)
            all_products.extend(products)
    
    # Process HomePod products
    for model in models_dict['homepod']:
        for region_code in REGIONS.keys():
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/shop/buy-homepod/{model}"
            products = extract_product_details(url, region_code)
            all_products.extend(products)
    
    return all_products

def merge_product_data(product_data):
    """
    Merge product data from all regions using SKU-based matching
    """
    df = pd.DataFrame(product_data)
    if df.empty:
        debug_print("No product data to merge!")
        return pd.DataFrame()
    
    region_dfs = {}
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        region_data = df[df['Region_Code'] == region_code].copy()
        region_data = region_data.drop_duplicates(subset='SKU')
        
        region_data.rename(columns={
            'Price': f'Price_{region_display}',
            'Name': f'Name_{region_display}',
            'PartNumber': f'PartNumber_{region_display}'
        }, inplace=True)
        region_dfs[region_code] = region_data
    
    ref_region = REFERENCE_REGION
    ref_display = REGIONS[ref_region][0]
    
    if ref_region not in region_dfs:
        return pd.DataFrame()
    
    merged_df = region_dfs[ref_region][['SKU', f'Price_{ref_display}', f'Name_{ref_display}']].copy()
    
    for region_code, region_df in region_dfs.items():
        if region_code == ref_region: continue
        
        region_display = REGIONS[region_code][0]
        columns_to_merge = ['SKU', f'Price_{region_display}', f'Name_{region_display}']
        merged_df = pd.merge(merged_df, region_df[columns_to_merge], on='SKU', how='outer')
    
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        merged_df[f'Price_{region_display}'] = merged_df[f'Price_{region_display}'].fillna(0)
        merged_df[f'Name_{region_display}'] = merged_df[f'Name_{region_display}'].fillna('')
    
    price_columns = [f'Price_{info[0]}' for code, info in REGIONS.items()]
    output_columns = ['SKU'] + price_columns + [f'Name_{ref_display}']
    output_df = merged_df[output_columns].copy()
    output_df = output_df.rename(columns={f'Name_{ref_display}': 'PRODUCT_NAME'})
    
    return output_df

def consolidate_similar_colors(df, price_tolerance=0.02):
    """
    Consolidate TV & Home products with same specs but different colors
    Removes color information completely for clean model-only output
    """
    if df.empty:
        return df
    
    # Find the product name column
    product_name_col = None
    for col in df.columns:
        if 'Name_' in col or col == 'PRODUCT_NAME':
            product_name_col = col
            break
    
    if not product_name_col:
        debug_print("No product name column found, skipping consolidation")
        return df
    
    # TV & Home color patterns (similar to other Apple products)
    color_patterns = [
        r'\b(space\s+gray|space\s+grey|midnight|starlight|silver|black|white)\b'
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
    base_names = []
    colors_list = []
    
    for idx, row in df_copy.iterrows():
        base_name, colors = extract_base_name_and_colors(row[product_name_col])
        base_names.append(base_name)
        colors_list.append(colors)
    
    df_copy['Base_Name'] = base_names
    df_copy['Colors'] = colors_list
    
    # Group by base name and consolidate
    consolidated_rows = []
    
    for base_name, group in df_copy.groupby('Base_Name'):
        if len(group) <= 1:
            # Single variant, keep as is
            for _, row in group.iterrows():
                consolidated_rows.append(row)
        else:
            # Multiple variants - consolidate if prices are similar
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
                # Don't consolidate - keep separate
                for _, row in group.iterrows():
                    consolidated_rows.append(row)
    
    # Create result DataFrame
    result_df = pd.DataFrame(consolidated_rows)
    
    # Remove helper columns
    result_df = result_df.drop(['Base_Name', 'Colors'], axis=1, errors='ignore')
    
    return result_df

def main():
    print("Starting Apple TV and Home product scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    all_products = get_all_products()
    merged_data = merge_product_data(all_products)
    
    # Apply color consolidation (remove color information)
    merged_data = consolidate_similar_colors(merged_data)
    
    print("\nResults:")
    print(merged_data)
    output_file = 'tvhome_products_merged.csv'
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved consolidated results to {output_file}")
    print(f"\nTotal unique products found: {len(merged_data)}")

if __name__ == "__main__":
    main()