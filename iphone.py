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
    Enhanced standardize product name for matching across regions (Future-Adaptive)
    
    Parameters:
    name (str): Original product name, e.g., "iPhone 17 Pro 1TB Cosmic Orange"
    
    Returns:
    str: Standardized name key, e.g., "iphone17pro_1tb_cosmicorange"
    """
    if not name:
        return ""

    # Convert to lowercase for processing
    name = name.lower()
    debug_print(f"Standardizing: '{name}'")

    # Enhanced capacity detection (supports future units like PB, EB)
    storage_match = re.search(r'(\d+)\s*(gb|tb|pb|eb)', name, re.IGNORECASE)
    
    # Enhanced model detection (supports iPhone Air, Ultra, Fold, etc.)
    # Priority order: specific patterns first, then fallback
    model_match = None
    
    # Special iPhone variants (Air, Ultra, Fold, etc.)
    special_variants = ['air', 'ultra', 'fold', 'mini', 'plus']
    for variant in special_variants:
        pattern = rf'iphone\s+({variant})(?:\s+(\d+(?:gb|tb|pb|eb)))?'
        match = re.search(pattern, name)
        if match:
            model_match = match
            break
    
    # iPhone with edition suffix (e.g., iPhone 16e)
    if not model_match:
        model_match = re.search(r'iphone\s*(\d+[a-z])(?:\s+([a-z\s]+?))?(?=\s*\d+\s*(?:gb|tb|pb|eb)|$)', name)
    
    # Standard iPhone pattern (iPhone 17, iPhone 17 Pro, iPhone 17 Pro Max)
    if not model_match:
        model_match = re.search(r'iphone\s*(\d+)(?:\s+([a-z\s]+?))?(?=\s*\d+\s*(?:gb|tb|pb|eb)|$)', name)
    
    # Fallback: any iPhone pattern
    if not model_match:
        model_match = re.search(r'iphone\s*([0-9a-z]+)(?:\s+([a-z\s]+))?', name)

    # Enhanced color extraction with expanded palette
    color_patterns = [
        # Basic colors
        'black', 'white', 'blue', 'pink', 'yellow', 'green', 'purple', 'red', 
        'silver', 'gold', 'orange', 'gray', 'grey',
        # Apple-specific colors
        'cosmic orange', 'deep blue', 'light gold', 'cloud white', 'space black', 
        'sky blue', 'midnight', 'starlight', 'alpine green', 'sierra blue',
        'product red', 'natural titanium', 'blue titanium', 'white titanium',
        'black titanium', 'desert titanium', 'natural', 'graphite'
    ]
    
    # Extract color by process of elimination
    name_copy = name
    if model_match:
        name_copy = name_copy.replace(model_match.group(0), "", 1)
    if storage_match:
        name_copy = name_copy.replace(storage_match.group(0), "", 1)
    
    # Find matching color (longest match first for compound colors)
    color = ""
    for color_pattern in sorted(color_patterns, key=len, reverse=True):
        if color_pattern in name_copy:
            color = color_pattern.replace(" ", "")
            break
    
    if not color:
        # Fallback: use whatever's left after removing model and storage
        color = name_copy.strip().replace(" ", "")
    
    # Create standardized key parts
    key_parts = []

    if model_match:
        model_num = model_match.group(1)
        model_variant = (model_match.group(2) or "").replace(" ", "")
        key_parts.append(f"iphone{model_num}{model_variant}")

    if storage_match:
        key_parts.append(f"{storage_match.group(1)}{storage_match.group(2).lower()}")

    if color:
        key_parts.append(color)

    result = "_".join(key_parts) if key_parts else name.replace(" ", "")
    debug_print(f"Standardized result: '{result}'")
    return result

def is_valid_iphone_model(model_id):
    """
    Validate if a discovered model ID is a real iPhone model (Future-Adaptive)
    
    Parameters:
    model_id (str): Model identifier like "iphone-17-pro" or just "17-pro"
    
    Returns:
    bool: True if it's a valid iPhone model
    """
    if not model_id or model_id == "":
        return False
    
    # Filter out known non-iPhone pages
    invalid_patterns = [
        'accessories', 'cases', 'chargers', 'airpods', 'watch', 
        'ipad', 'mac', 'compare', 'trade-in', 'carrier-offers',
        'gift-card', 'financing', 'support'
    ]
    
    model_lower = model_id.lower()
    for pattern in invalid_patterns:
        if pattern in model_lower:
            return False
    
    # Add iphone- prefix if missing for pattern matching
    if not model_id.startswith('iphone-'):
        model_id = f"iphone-{model_id}"
    
    model_part = model_id.replace('iphone-', '')
    
    # Valid model patterns (adaptive to future models)
    valid_patterns = [
        r'^\d+$',                    # iPhone 17
        r'^\d+[a-z]+$',             # iPhone 16e, 17c
        r'^\d+-pro$',               # iPhone 17-pro
        r'^\d+-pro-max$',           # iPhone 17-pro-max
        r'^\d+-plus$',              # iPhone 17-plus
        r'^(air|ultra|fold|mini)$', # iPhone Air, Ultra, etc.
        r'^(air|ultra|fold|mini)-\d+$',  # iPhone Air-2 (if they version them)
    ]
    
    for pattern in valid_patterns:
        if re.match(pattern, model_part, re.IGNORECASE):
            return True
    
    debug_print(f"Unknown model pattern: {model_id}")
    return False

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
            # Relaxed check: match any link under buy-iphone, not just those starting with iphone-
            if '/shop/buy-iphone/' in href:
                # Extract model part
                parts = href.split('buy-iphone/')
                if len(parts) > 1:
                    model = parts[1].split('?')[0].split('#')[0]
                    # Basic validation to avoid empty strings or parent directory
                    if model and model != "":
                        iphone_links.append(model)

        # Filter and validate models
        unique_models = list(set(iphone_links))
        valid_models = [model for model in unique_models if is_valid_iphone_model(model)]

        if not valid_models:
            debug_print(f"Could not find valid iPhone models at {url}, using default model list")
            return default_models

        debug_print(f"Discovered valid models: {', '.join(valid_models)}")
        return valid_models

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
                        
                        # Derive BaseSKU (useful context, even if not main merge key yet)
                        base_sku = sku 
                        if part_number:
                             base_sku = re.sub(r'[A-Z]{2}/[A-Z]$', '', part_number)
                             base_sku = re.sub(r'/[A-Z]$', '', base_sku)

                        # Generate standardized name for matching products across regions (Legacy logic preserved)
                        std_name = standardize_product_name(name)
                        
                        product_details.append({
                            "SKU": sku,
                            "BaseSKU": base_sku,
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
    except Exception as e:
        debug_print(f"Error parsing product data: {e}")
        return []

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
            # Multi-strategy JSON extraction (Future-Adaptive)
            json_str = ""
            extraction_method = "unknown"
            
            # Strategy 2a: Enhanced regex patterns (try multiple patterns)
            regex_patterns = [
                # Pattern 1: productSelectionData: {...}, displayValues
                r'productSelectionData:\s*(\{.*?\})\s*,\s*displayValues',
                # Pattern 2: productSelectionData: {...} (without displayValues)
                r'productSelectionData:\s*(\{[^}]*(?:\{[^}]*\}[^}]*)*\})',
                # Pattern 3: More flexible whitespace handling
                r'productSelectionData\s*:\s*(\{.*?\})\s*[,;}]',
            ]
            
            for i, pattern in enumerate(regex_patterns):
                match = re.search(pattern, script_content, re.DOTALL)
                if match:
                    json_str = match.group(1)
                    extraction_method = f"regex_pattern_{i+1}"
                    debug_print(f"JSON extracted using {extraction_method}")
                    break
            
            # Strategy 2b: Enhanced brace counting fallback
            if not json_str:
                debug_print("Regex patterns failed, trying enhanced brace counting")
                key_index = script_content.find('productSelectionData:')
                if key_index != -1:
                    # Look for opening brace after the key
                    start_index = script_content.find('{', key_index)
                    if start_index != -1:
                        brace_count = 0
                        quote_count = 0
                        in_string = False
                        escape_next = False
                        
                        for i in range(start_index, len(script_content)):
                            char = script_content[i]
                            
                            # Handle string escapes
                            if escape_next:
                                escape_next = False
                                json_str += char
                                continue
                            
                            if char == '\\' and in_string:
                                escape_next = True
                                json_str += char
                                continue
                            
                            # Track string boundaries
                            if char == '"':
                                in_string = not in_string
                            
                            # Only count braces outside of strings
                            if not in_string:
                                if char == '{':
                                    brace_count += 1
                                elif char == '}':
                                    brace_count -= 1
                            
                            json_str += char
                            
                            # Break when braces are balanced
                            if brace_count == 0:
                                extraction_method = "enhanced_brace_counting"
                                debug_print(f"JSON extracted using {extraction_method}")
                                break
            
            # Strategy 2c: Validate and parse JSON
            if json_str:
                try:
                    bootstrap_data = json.loads(json_str)
                    debug_print(f"JSON parsing successful (method: {extraction_method})")
                except json.JSONDecodeError as e:
                    debug_print(f"JSON parsing failed (method: {extraction_method}): {e}")
                    debug_print(f"JSON snippet (first 200 chars): {json_str[:200]}...")
                    return []
                
                # Process the bootstrap data
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
                        if not name:
                            name = soup.find('title').text.split('-')[0].strip() if soup.find('title') else "Unknown Product"
                        
                        # Use basePartNumber as SKU if available, else derive
                        base_sku = base_part_number
                        if not base_sku and part_number:
                                base_sku = re.sub(r'[A-Z]{2}/[A-Z]$', '', part_number)
                                base_sku = re.sub(r'/[A-Z]$', '', base_sku)
                        
                        std_name = standardize_product_name(name)
                        
                        product_details.append({
                            "SKU": part_number,
                            "BaseSKU": base_sku,
                            "Name": name,
                            "Price": price_val,
                            "Region": region_display,
                            "Region_Code": region_code,
                            "PartNumber": part_number,
                            "Standardized_Name": std_name
                        })
                    return product_details
        except Exception as e:
            debug_print(f"Error parsing bootstrap JSON: {e}")

    return product_details

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

def consolidate_similar_colors(df, price_tolerance=0.02):
    """ROBUST color consolidation - bulletproof version"""
    from robust_consolidation import robust_consolidate_colors
    return robust_consolidate_colors(df, price_tolerance, debug=False)

def generate_plot(df, filename='price_diff.png'):
    """Generate price difference chart"""
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Filter valid data
        plot_df = df[(df['Price_US'] > 0) & (df['Price_TW'] > 0)].copy()
        
        if plot_df.empty:
            debug_print("No data available for plotting")
            return

        # Approx exchange rate (can be fetched dynamically later)
        EXCHANGE_RATE = 32.0 
        plot_df['Diff_USD'] = (plot_df['Price_TW'] / EXCHANGE_RATE) - plot_df['Price_US']
        
        # Sort and take top 15
        plot_df = plot_df.sort_values('Diff_USD', ascending=False).head(15)
        
        plt.figure(figsize=(14, 10))
        sns.set_style("whitegrid")
        
        # Bar chart
        ax = sns.barplot(x='Diff_USD', y='PRODUCT_NAME', data=plot_df, hue='PRODUCT_NAME', legend=False, palette='viridis')
        
        plt.title(f'TW vs US Price Difference (USD) - Rate: {EXCHANGE_RATE}', fontsize=16)
        plt.xlabel('Difference (USD) - Positive = TW is more expensive', fontsize=12)
        plt.ylabel('')
        
        # Labels
        for i, v in enumerate(plot_df['Diff_USD']):
            ax.text(v + 5, i, f"+${v:.0f}", va='center')
            
        plt.tight_layout()
        plt.savefig(filename)
        print(f"\nChart saved to {filename}")
        
    except ImportError:
        print("\n[WARN] matplotlib/seaborn not installed, skipping plot.")
    except Exception as e:
        print(f"\n[WARN] Plotting failed: {e}")

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
    
    # Apply color consolidation (reduce visual noise)
    merged_data = consolidate_similar_colors(merged_data)
    
    # Save consolidated results to CSV
    output_file = 'iphone_products_merged.csv'
    merged_data.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\nSaved consolidated results to {output_file}")
    
    # Generate Plot
    generate_plot(merged_data)
    
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