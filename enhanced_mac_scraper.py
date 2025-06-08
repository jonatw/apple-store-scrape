#!/usr/bin/env python3
"""
Enhanced Mac scraper that extracts detailed specifications from Apple's website
This version extracts CPU, storage, memory, and other specifications from HTML elements
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re

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

def extract_specs_from_text(text):
    """
    Extract detailed specifications from text using regex patterns
    """
    specs = {
        'chip': '',
        'cpu_cores': '',
        'gpu_cores': '',
        'neural_engine': '',
        'memory': '',
        'storage': '',
        'display': '',
        'ports': ''
    }
    
    if not text:
        return specs
    
    text_lower = text.lower()
    
    # Extract chip information (M1, M2, M3, M4 with variants)
    chip_patterns = [
        r'apple\s+(m[1-4](?:\s+(?:pro|max|ultra))?)\s+chip',
        r'(m[1-4](?:\s+(?:pro|max|ultra))?)\s+chip',
        r'(m[1-4](?:\s+(?:pro|max|ultra))?)\s+processor'
    ]
    for pattern in chip_patterns:
        chip_match = re.search(pattern, text_lower)
        if chip_match:
            specs['chip'] = chip_match.group(1).upper().replace(' ', ' ')
            break
    
    # Extract CPU cores
    cpu_pattern = r'(\d+)-core\s+cpu'
    cpu_match = re.search(cpu_pattern, text_lower)
    if cpu_match:
        specs['cpu_cores'] = f"{cpu_match.group(1)}-core"
    
    # Extract GPU cores
    gpu_pattern = r'(\d+)-core\s+gpu'
    gpu_match = re.search(gpu_pattern, text_lower)
    if gpu_match:
        specs['gpu_cores'] = f"{gpu_match.group(1)}-core"
    
    # Extract Neural Engine
    neural_pattern = r'(\d+)-core\s+neural\s+engine'
    neural_match = re.search(neural_pattern, text_lower)
    if neural_match:
        specs['neural_engine'] = f"{neural_match.group(1)}-core"
    
    # Extract memory
    memory_patterns = [
        r'(\d+)gb\s+(?:unified\s+)?memory',
        r'memory[:\s]+(\d+)gb',
        r'(\d+)gb\s+memory'
    ]
    for pattern in memory_patterns:
        memory_match = re.search(pattern, text_lower)
        if memory_match:
            specs['memory'] = f"{memory_match.group(1)}GB"
            break
    
    # Extract storage
    storage_patterns = [
        r'(\d+)(gb|tb)\s+storage',
        r'storage[:\s]+(\d+)(gb|tb)',
        r'(\d+)(gb|tb)\s+ssd'
    ]
    for pattern in storage_patterns:
        storage_match = re.search(pattern, text_lower)
        if storage_match:
            amount = storage_match.group(1)
            unit = storage_match.group(2).upper()
            specs['storage'] = f"{amount}{unit}"
            break
    
    # Extract display information
    display_patterns = [
        r'(\d+(?:\.\d+)?)-inch.*?display',
        r'(\d+(?:\.\d+)?).*?retina\s+display'
    ]
    for pattern in display_patterns:
        display_match = re.search(pattern, text_lower)
        if display_match:
            specs['display'] = f"{display_match.group(1)}\""
            break
    
    return specs

def extract_product_specs_from_html(soup, sku_to_match=None):
    """
    Extract product specifications from HTML elements
    """
    product_specs = []
    
    # Look for dimension elements that contain configuration information
    dimension_elements = soup.find_all(attrs={'class': re.compile(r'.*dimension.*', re.I)})
    
    for elem in dimension_elements:
        text = elem.get_text(strip=True)
        
        # Skip empty or very short text
        if not text or len(text) < 20:
            continue
        
        # Look for text that contains chip/processor information
        if 'chip' in text.lower() or 'processor' in text.lower():
            specs = extract_specs_from_text(text)
            
            # Only add if we extracted meaningful specifications
            if any(specs.values()):
                # Try to associate with a specific product by looking for nearby SKU information
                product_info = {
                    'config_text': text,
                    'specs': specs
                }
                product_specs.append(product_info)
                debug_print(f"Found spec: {text}")
    
    return product_specs

def get_available_models(region_code=""):
    """Get available Mac models from Apple store page"""
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-mac"
    
    default_models = ["mac-mini", "imac"]  # Test with these models
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Cannot access {url}, using default model list")
            return default_models

        soup = BeautifulSoup(response.text, 'html.parser')
        mac_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if '/shop/buy-mac/' in href:
                model = href.split('buy-mac/')[1].split('?')[0].split('#')[0]
                if not any(x in model for x in ['compare', 'accessories', 'help', 'financing']):
                    mac_links.append(model)

        unique_models = list(set(mac_links))
        if not unique_models:
            debug_print(f"Could not find Mac models at {url}, using default model list")
            return default_models

        return unique_models

    except Exception as e:
        debug_print(f"Error getting Mac models: {e}, using default model list")
        return default_models

def extract_product_details(url, region_code=""):
    """
    Extract product details including specifications from Apple store page
    """
    time.sleep(REQUEST_DELAY)
    
    region_display = REGIONS.get(region_code, ["Unknown"])[0]
    debug_print(f"Fetching products from {url} for region {region_display}")
    
    response = requests.get(url)
    if response.status_code != 200:
        debug_print(f"Failed to retrieve {url}. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Get basic product data from JSON
    json_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
    if not json_script:
        debug_print(f"No matching script found in {url}")
        return []

    try:
        json_data = json.loads(json_script.string)
        data = json_data.get('data', {})
        products = data.get('products', [])
        
        debug_print(f"Found {len(products)} products for region {region_display}")
        
        # Extract specifications from HTML
        html_specs = extract_product_specs_from_html(soup)
        debug_print(f"Extracted {len(html_specs)} spec configurations from HTML")
        
        # Create detailed product list
        product_details = []
        
        # If we have HTML specs, try to match them with products
        if html_specs and products:
            # For each spec configuration, create product variants
            for i, product in enumerate(products):
                sku = product.get("sku")
                name = product.get("name", "")
                price = product.get("price", {}).get("fullPrice")
                part_number = product.get("partNumber", "")
                
                # Try to match with HTML specs based on price ranges or position
                if i < len(html_specs):
                    html_spec = html_specs[i % len(html_specs)]
                    specs = html_spec['specs']
                else:
                    # Use basic spec extraction if no HTML match
                    specs = {
                        'chip': '',
                        'cpu_cores': '',
                        'gpu_cores': '',
                        'neural_engine': '',
                        'memory': '',
                        'storage': '',
                        'display': '',
                        'ports': ''
                    }
                
                product_details.append({
                    "SKU": sku,
                    "Name": name,
                    "Price": price,
                    "Chip": specs["chip"],
                    "CPU": specs["cpu_cores"],
                    "GPU": specs["gpu_cores"],
                    "Neural_Engine": specs["neural_engine"],
                    "Memory": specs["memory"],
                    "Storage": specs["storage"],
                    "Display": specs["display"],
                    "Region": region_display,
                    "Region_Code": region_code,
                    "PartNumber": part_number
                })
        else:
            # Fallback to basic product extraction
            for product in products:
                sku = product.get("sku")
                name = product.get("name", "")
                price = product.get("price", {}).get("fullPrice")
                part_number = product.get("partNumber", "")
                
                product_details.append({
                    "SKU": sku,
                    "Name": name,
                    "Price": price,
                    "Chip": "",
                    "CPU": "",
                    "GPU": "",
                    "Neural_Engine": "",
                    "Memory": "",
                    "Storage": "",
                    "Display": "",
                    "Region": region_display,
                    "Region_Code": region_code,
                    "PartNumber": part_number
                })
        
        return product_details
        
    except Exception as e:
        debug_print(f"Error parsing product data: {e}")
        return []

def get_all_products():
    """Get all products from all configured regions"""
    all_models = set()
    for region_code in REGIONS.keys():
        models = get_available_models(region_code)
        all_models.update(models)
    
    debug_print(f"Found models across all regions: {', '.join(all_models)}")
    
    all_products = []
    for model in all_models:
        for region_code in REGIONS.keys():
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/shop/buy-mac/{model}"
            products = extract_product_details(url, region_code)
            all_products.extend(products)
    
    return all_products

def merge_product_data(product_data):
    """Merge product data from all regions using SKU-based matching"""
    df = pd.DataFrame(product_data)
    
    if df.empty:
        debug_print("No product data to merge!")
        return pd.DataFrame()
    
    # Create separate DataFrames for each region
    region_dfs = {}
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        region_data = df[df['Region_Code'] == region_code].copy()
        
        region_data = region_data.drop_duplicates(subset='SKU')
        
        # Rename price column to include region
        region_data.rename(columns={
            'Price': f'Price_{region_display}',
            'Name': f'Name_{region_display}'
        }, inplace=True)
        
        region_dfs[region_code] = region_data
    
    # Start with the reference region
    ref_region = REFERENCE_REGION
    ref_display = REGIONS[ref_region][0]
    
    if ref_region not in region_dfs:
        debug_print(f"Reference region {ref_display} not found in data!")
        return pd.DataFrame()
    
    # Get the base dataframe with specifications
    base_columns = ['SKU', f'Price_{ref_display}', f'Name_{ref_display}', 
                   'Chip', 'CPU', 'GPU', 'Neural_Engine', 'Memory', 'Storage', 'Display']
    available_columns = [col for col in base_columns if col in region_dfs[ref_region].columns]
    merged_df = region_dfs[ref_region][available_columns].copy()
    
    # Merge with other regions using SKU as the key
    for region_code, region_df in region_dfs.items():
        if region_code == ref_region:
            continue
        
        region_display = REGIONS[region_code][0]
        columns_to_merge = ['SKU', f'Price_{region_display}']
        
        merged_df = pd.merge(
            merged_df, 
            region_df[columns_to_merge], 
            on='SKU', 
            how='outer'
        )
    
    # Fill missing values
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        price_col = f'Price_{region_display}'
        if price_col in merged_df.columns:
            merged_df[price_col] = merged_df[price_col].fillna(0)
    
    # Reorder columns for better readability
    output_columns = ['SKU', 'Chip', 'CPU', 'GPU', 'Neural_Engine', 'Memory', 'Storage', 'Display']
    
    # Add price columns
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        price_col = f'Price_{region_display}'
        if price_col in merged_df.columns:
            output_columns.append(price_col)
    
    # Add product name
    name_col = f'Name_{ref_display}'
    if name_col in merged_df.columns:
        output_columns.append('PRODUCT_NAME')
        merged_df = merged_df.rename(columns={name_col: 'PRODUCT_NAME'})
    
    # Select only available columns
    available_output_columns = [col for col in output_columns if col in merged_df.columns]
    output_df = merged_df[available_output_columns].copy()
    
    return output_df

def main():
    """Main execution function"""
    print("Starting Enhanced Mac Product Scraper...")
    print(f"Configured regions: {', '.join([info[0] for info in REGIONS.values()])}")
    
    # Get all products from all regions
    all_products = get_all_products()
    
    # Merge product data
    merged_data = merge_product_data(all_products)
    
    # Display results
    print("\nResults:")
    print(merged_data.to_string())
    
    # Save to CSV
    output_file = 'enhanced_mac_products.csv'
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