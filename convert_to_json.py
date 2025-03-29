#!/usr/bin/env python3
"""
CSV to JSON Converter for Apple Store Scraper
Converts CSV data to structured JSON for web display

This script requires the same dependencies as the main scraper:
- pandas==2.2.3
"""

import pandas as pd
import json
import os
from datetime import datetime
import sys

# Configure exchange rate information (can be dynamically fetched via API in the future)
EXCHANGE_RATES = {
    "USD": 1.0,
    "TWD": 31.5  # 1 USD ≈ 31.5 TWD (can be adjusted according to actual exchange rate)
}

def csv_to_json(csv_file, json_file, product_type):
    """
    Convert CSV file to structured JSON file
    
    Parameters:
    csv_file (str): Path to input CSV file
    json_file (str): Path to output JSON file
    product_type (str): Product type ('iphone' or 'ipad')
    """
    print(f"Processing {csv_file}...")
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: File {csv_file} not found!")
        return False
    
    try:
        # Read CSV
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        
        # Check data format
        if df.empty:
            print(f"Warning: {csv_file} contains no data")
            return False
            
        # Identify region columns (assuming format Price_XX)
        price_cols = [col for col in df.columns if col.startswith('Price_')]
        regions = [col.replace('Price_', '') for col in price_cols]
        
        print(f"Detected regions: {', '.join(regions)}")
        
        # Prepare product list
        products = df.to_dict(orient='records')
        
        # Add product type marker
        for p in products:
            p['product_type'] = product_type
            
            # Process price difference percentage
            if 'Price_US' in p and 'Price_TW' in p:
                usd_price = p['Price_US'] or 0
                twd_price = p['Price_TW'] or 0
                
                if usd_price > 0:
                    # Convert TWD to USD for comparison
                    twd_in_usd = twd_price / EXCHANGE_RATES['TWD']
                    diff_percent = ((twd_in_usd - usd_price) / usd_price) * 100
                    p['price_difference_percent'] = round(diff_percent, 1)
                else:
                    p['price_difference_percent'] = 0
        
        # Create complete JSON structure
        data = {
            "metadata": {
                "lastUpdated": datetime.now().isoformat(),
                "exchangeRates": EXCHANGE_RATES,
                "regions": regions,
                "productType": product_type,
                "totalProducts": len(products)
            },
            "products": products
        }
        
        # Ensure output directories exist
        base_dir = os.path.dirname(json_file)
        src_dir = os.path.join("src", base_dir)
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(src_dir, exist_ok=True)
        
        # Determine the src path version
        src_json_file = os.path.join("src", json_file)
        
        # Write JSON files to both directories
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        with open(src_json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully converted {csv_file} to {json_file} and {src_json_file}")
        print(f"Total products: {len(products)}")
        return True
        
    except Exception as e:
        print(f"Error converting {csv_file}: {str(e)}")
        return False

def main():
    """Main program entry point"""
    print("CSV to JSON Converter for Apple Store Scraper")
    print("=" * 50)
    
    # Ensure both data directories exist
    data_dir = "data"
    src_data_dir = "src/data"
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(src_data_dir, exist_ok=True)
    
    # Convert iPhone data
    iphone_success = csv_to_json(
        "iphone_products_merged.csv", 
        os.path.join(data_dir, "iphone_data.json"),
        "iphone"
    )
    
    # Convert iPad data
    ipad_success = csv_to_json(
        "ipad_products_merged.csv", 
        os.path.join(data_dir, "ipad_data.json"),
        "ipad"
    )
    
    # Generate index file containing references to all datasets
    index = {
        "lastUpdated": datetime.now().isoformat(),
        "datasets": []
    }
    
    if iphone_success:
        index["datasets"].append({
            "type": "iphone",
            "file": "iphone_data.json",
            "title": "iPhone Models"
        })
    
    if ipad_success:
        index["datasets"].append({
            "type": "ipad",
            "file": "ipad_data.json",
            "title": "iPad Models"
        })
    
    # Write index file to both directories
    with open(os.path.join(data_dir, "index.json"), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
        
    with open(os.path.join(src_data_dir, "index.json"), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print("\nCreated data index files: data/index.json and src/data/index.json")
    
    if iphone_success or ipad_success:
        print("\nConversion completed successfully!")
    else:
        print("\nNo data was converted!")
        sys.exit(1)

if __name__ == "__main__":
    main()