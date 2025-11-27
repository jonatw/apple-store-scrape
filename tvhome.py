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

def main():
    print("Starting Apple TV and Home product scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    all_products = get_all_products()
    merged_data = merge_product_data(all_products)
    print("\nResults:")
    print(merged_data)
    output_file = 'tvhome_products_merged.csv'
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved results to {output_file}")
    print(f"\nTotal unique products found: {len(merged_data)}")

if __name__ == "__main__":
    main()