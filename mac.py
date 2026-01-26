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

def extract_specs_from_text(text):
    """Extract detailed specifications from configuration text"""
    specs = {
        'chip': '',
        'cpu_cores': '',
        'gpu_cores': '',
        'neural_engine': '',
        'memory': '',
        'storage': '',
    }
    
    if not text:
        return specs
    
    text_lower = text.lower()
    
    # Extract chip information (M1, M2, M3, M4 with variants)
    chip_patterns = [
        r'apple\s+(m[1-4](?:\s+(?:pro|max|ultra))?)\s+chip',
        r'(m[1-4](?:\s+(?:pro|max|ultra))?)\s+chip'
    ]
    for pattern in chip_patterns:
        match = re.search(pattern, text_lower)
        if match:
            specs['chip'] = match.group(1).upper().replace('  ', ' ')
            break
    
    # Extract CPU cores
    cpu_match = re.search(r'(\d+)-core\s+cpu', text_lower)
    if cpu_match:
        specs['cpu_cores'] = cpu_match.group(1)
    
    # Extract GPU cores  
    gpu_match = re.search(r'(\d+)-core\s+gpu', text_lower)
    if gpu_match:
        specs['gpu_cores'] = gpu_match.group(1)
    
    # Extract Neural Engine
    neural_match = re.search(r'(\d+)-core\s+neural\s+engine', text_lower)
    if neural_match:
        specs['neural_engine'] = neural_match.group(1)
    
    # Extract memory with flexible patterns
    memory_patterns = [
        r'(\d+)gb\s+(?:unified\s+)?memory',
        r'(\d+)gb\s+memory',
        r'memory[:\s]*(\d+)gb'
    ]
    for pattern in memory_patterns:
        match = re.search(pattern, text_lower)
        if match:
            specs['memory'] = f"{match.group(1)}GB"
            break
    
    # Extract storage
    storage_patterns = [
        r'(\d+)(gb|tb)\s+storage',
        r'storage[:\s]*(\d+)(gb|tb)'
    ]
    for pattern in storage_patterns:
        match = re.search(pattern, text_lower)
        if match:
            amount = match.group(1)
            unit = match.group(2).upper()
            specs['storage'] = f"{amount}{unit}"
            break
    
    return specs

def extract_enhanced_product_specs(soup):
    """Extract product specifications with better matching"""
    
    # Find all product configuration texts
    config_texts = []
    
    # Look for dimension elements with chip/processor information
    dimension_elements = soup.find_all(attrs={'class': re.compile(r'.*dimension.*', re.I)})
    
    for elem in dimension_elements:
        text = elem.get_text(strip=True)
        
        # Filter for meaningful configuration text
        if ('chip' in text.lower() or 'processor' in text.lower()) and len(text) > 30:
            # Clean up the text (remove color selections, etc.)
            clean_text = re.sub(r'(blue|purple|pink|orange|yellow|green|silver)+', '', text, flags=re.IGNORECASE)
            clean_text = re.sub(r'select a finish', '', clean_text, flags=re.IGNORECASE)
            clean_text = re.sub(r'\s+', ' ', clean_text).strip()
            
            if clean_text not in config_texts:  # Avoid duplicates
                config_texts.append(clean_text)
                debug_print(f"Found config: {clean_text}")
    
    # Extract specifications from each configuration
    spec_variants = []
    for config_text in config_texts:
        specs = extract_specs_from_text(config_text)
        if any(specs.values()):  # Only add if we found meaningful specs
            spec_variants.append(specs)
    
    return spec_variants

def match_products_with_specs(products, spec_variants):
    """Match JSON products with extracted specifications based on price tiers"""
    
    if not spec_variants:
        return [{**p, 'specs': {
            'chip': '', 'cpu_cores': '', 'gpu_cores': '', 
            'neural_engine': '', 'memory': '', 'storage': ''
        }} for p in products]
    
    # 1. Group products by price
    products_by_price = {}
    for p in products:
        price = p.get('price', {}).get('fullPrice', 0)
        if price not in products_by_price:
            products_by_price[price] = []
        products_by_price[price].append(p)
        
    # 2. Sort price tiers
    sorted_prices = sorted(products_by_price.keys())
    
    # 3. Sort specs by "value" (Storage > Memory > CPU > GPU)
    def spec_sort_key(specs):
        # Extract numeric values for sorting
        def get_num(text, unit=''):
            if not text: return 0
            
            # Handle split only if unit is provided
            source_text = text
            if unit:
                parts = text.split(unit)
                if parts:
                    source_text = parts[0]
            
            # Remove non-numeric
            clean = re.sub(r'[^\d]', '', source_text)
            return int(clean) if clean else 0
            
        storage = get_num(specs.get('storage', ''), 'GB')
        if 'TB' in specs.get('storage', ''): storage *= 1000
        
        memory = get_num(specs.get('memory', ''))
        cpu = get_num(specs.get('cpu_cores', ''))
        
        return (storage, memory, cpu)
    
    sorted_specs = sorted(spec_variants, key=spec_sort_key)
    
    # 4. Assign specs to price tiers
    matched_products = []
    
    # If we have mismatch in counts, we try our best to align
    # Usually: Lowest Price -> Lowest Spec
    
    for i, price in enumerate(sorted_prices):
        products_in_tier = products_by_price[price]
        
        # Find matching spec
        # If we have enough specs, take the ith one.
        # If not, reuse the last one (for highest tiers) or map proportionally.
        if i < len(sorted_specs):
            assigned_specs = sorted_specs[i]
        else:
            # Fallback: use the highest spec for remaining high price tiers
            assigned_specs = sorted_specs[-1]
            
        # Assign this spec to ALL products in this price tier
        for product in products_in_tier:
            matched_products.append({
                **product,
                'specs': assigned_specs
            })
            
    return matched_products

def get_available_models(region_code=""):
    """
    Get available Mac models from Apple store page
    
    Parameters:
    region_code (str): Region code, e.g., "tw" for Taiwan, "" for US
    
    Returns:
    list: List of available Mac models, e.g., ["macbook-air", "macbook-pro", ...]
    """
    region_prefix = f"/{region_code}" if region_code else ""
    url = f"https://www.apple.com{region_prefix}/shop/buy-mac"
    
    # Focus on main Mac products for better results
    default_models = ["mac-mini", "imac", "mac-studio"]
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            debug_print(f"Cannot access {url}, using default model list")
            return default_models

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links to buy-mac pages
        mac_links = []
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if '/shop/buy-mac/' in href:
                # Extract model part (e.g., extract macbook-air from /tw/shop/buy-mac/macbook-air)
                model = href.split('buy-mac/')[1].split('?')[0].split('#')[0]
                # Filter out non-product links
                if not any(x in model for x in ['compare', 'accessories', 'help', 'financing']):
                    mac_links.append(model)

        # Remove duplicates and return
        unique_models = list(set(mac_links))

        if unique_models:
            # Filter to main Mac computers only (exclude displays)
            main_models = [m for m in unique_models if m in ['mac-mini', 'imac', 'mac-studio', 'macbook-air', 'macbook-pro'] or 'mac-pro' in m]
            return main_models if main_models else default_models
        else:
            debug_print(f"Could not find Mac models at {url}, using default model list")
            return default_models

    except Exception as e:
        debug_print(f"Error getting Mac models: {e}, using default model list")
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
        debug_print(f"No JSON data found in {url}")
        return []

    # Parse JSON content
    try:
        json_data = json.loads(json_script.string)
        data = json_data.get('data', {})
        products = data.get('products', [])
        
        debug_print(f"Found {len(products)} products for region {region_display}")
        
        # Extract specifications from HTML
        spec_variants = extract_enhanced_product_specs(soup)
        debug_print(f"Extracted {len(spec_variants)} spec variants from HTML")
        
        # Match products with specifications
        matched_products = match_products_with_specs(products, spec_variants)
        
        # Create detailed product list
        product_details = []
        
        for product_with_specs in matched_products:
            sku = product_with_specs.get("sku")
            name = product_with_specs.get("name", "")
            price = product_with_specs.get("price", {}).get("fullPrice")
            part_number = product_with_specs.get("partNumber", "")
            specs = product_with_specs.get("specs", {})
            
            product_details.append({
                "SKU": sku,
                "Name": name,
                "Price": price,
                "Chip": specs.get("chip", ""),
                "CPU_Cores": specs.get("cpu_cores", ""),
                "GPU_Cores": specs.get("gpu_cores", ""),
                "Neural_Engine": specs.get("neural_engine", ""),
                "Memory": specs.get("memory", ""),
                "Storage": specs.get("storage", ""),
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
    # Only get models from US to avoid duplicates in discovery
    models = get_available_models("")
    debug_print(f"Found models: {', '.join(models)}")
    
    # Fetch products for each model from each region
    all_products = []
    for model in models:
        for region_code in REGIONS.keys():
            region_prefix = f"/{region_code}" if region_code else ""
            url = f"https://www.apple.com{region_prefix}/shop/buy-mac/{model}"
            products = extract_product_details(url, region_code)
            all_products.extend(products)
    
    return all_products

def merge_product_data(product_data):
    """
    Merge product data from all regions using SKU-based matching (like iPad)
    
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
    
    # Get the base dataframe with specifications
    base_columns = ['SKU', f'Price_{ref_display}', f'Name_{ref_display}', 
                   'Chip', 'CPU_Cores', 'GPU_Cores', 'Neural_Engine', 'Memory', 'Storage']
    available_columns = [col for col in base_columns if col in region_dfs[ref_region].columns]
    merged_df = region_dfs[ref_region][available_columns].copy()
    
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
    
    # Reorder columns for better readability
    output_columns = ['SKU', 'Chip', 'CPU_Cores', 'GPU_Cores', 'Neural_Engine', 'Memory', 'Storage']
    
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

# ==================== MAIN EXECUTION ====================

def consolidate_similar_colors(df, price_tolerance=0.02):
    """
    Consolidate Mac products with same specs but different colors
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
    
    # Mac-specific color patterns (simpler than other products)
    color_patterns = [
        r'\b(space\s+gray|space\s+grey|midnight|starlight)\b',
        r'\b(silver|gold|rose\s+gold|black|white)\b',
        r'\b(natural|graphite|jet\s+black)\b'
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
    print("Starting Mac product scraper...")
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
    output_file = 'mac_products_merged.csv'
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved consolidated results to {output_file}")
    
    # Display statistics
    print(f"\nTotal unique products found: {len(merged_data)}")
    
    # Show specification coverage
    spec_columns = ['Chip', 'CPU_Cores', 'GPU_Cores', 'Memory', 'Storage']
    for col in spec_columns:
        if col in merged_data.columns:
            filled = (merged_data[col] != '').sum()
            total = len(merged_data)
            percentage = (filled / total * 100) if total > 0 else 0
            print(f"{col} specifications found: {filled}/{total} ({percentage:.1f}%)")
    
    # Regional pricing info
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        price_col = f'Price_{region_display}'
        
        if price_col in merged_data.columns:
            non_zero_prices = (merged_data[price_col] > 0).sum()
            print(f"Products found in {region_display}: {non_zero_prices}")

if __name__ == "__main__":
    main()