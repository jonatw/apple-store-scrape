#!/usr/bin/env python3
"""
CSV to JSON Converter for Apple Store Scraper
Converts CSV data to structured JSON for web display

This script requires the following dependencies:
- pandas==2.2.3
- requests
- beautifulsoup4
"""

import pandas as pd
import json
import os
import re
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime

# URL for Cathay Bank exchange rate page
EXCHANGE_RATE_URL = "https://accessibility.cathaybk.com.tw/exchange-rate-search.aspx"

def fetch_exchange_rate(debug=False):
    """
    Fetch the current USD/TWD exchange rate from Cathay Bank
    Returns the selling rate (used for credit card transactions)
    """
    try:
        # Send request to the exchange rate page
        if debug:
            print(f"Requesting URL: {EXCHANGE_RATE_URL}")
        response = requests.get(EXCHANGE_RATE_URL)
        if response.status_code != 200:
            print(f"Error: Failed to access exchange rate page. Status code: {response.status_code}")
            return None
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the div with ID MainContent_tab_rate_realtime
        rate_div = soup.find('div', {'id': 'MainContent_tab_rate_realtime'})
        if not rate_div:
            if debug:
                print("HTML structure:")
                print(soup.prettify()[:1000])  # Print first 1000 chars of HTML
            print("Error: Could not find rate div with ID 'MainContent_tab_rate_realtime'")
            return None
            
        # Find the table inside this div
        table = rate_div.find('table')
        if not table:
            if debug:
                print("Rate div contents:")
                print(rate_div.prettify())
            print("Error: Could not find exchange rate table")
            return None
        
        # Find the row with USD
        usd_row = None
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if cells and '美元(USD)' in cells[0].text:
                usd_row = row
                break
        
        if not usd_row:
            print("Error: Could not find USD exchange rate row")
            return None
        
        # Get all cells from the row
        cells = usd_row.find_all('td')
        
        # The selling rate is in the third column (index 2)
        if len(cells) >= 3:
            selling_rate = cells[2].text.strip()
            # Convert to float, removing any non-numeric characters
            selling_rate = float(re.sub(r'[^\d.]', '', selling_rate))
            print(f"Successfully fetched USD/TWD exchange rate: {selling_rate}")
            return selling_rate
        else:
            print("Error: Could not find selling rate in USD row")
            return None
            
    except Exception as e:
        print(f"Error fetching exchange rate: {str(e)}")
        return None

def get_exchange_rates(debug=False):
    """
    Get exchange rates - either fetch current rates or use defaults
    """
    exchange_rates = {
        "USD": 1.0,
        "TWD": 31.5,  # Default fallback value
        "lastUpdated": datetime.now().isoformat(),
        "source": "Cathay Bank"
    }
    
    # Ensure the data directory exists
    data_dir = "src/data"
    os.makedirs(data_dir, exist_ok=True)
    exchange_rate_file = os.path.join(data_dir, "exchange_rate.json")
    
    # Try to fetch current exchange rate
    print("Fetching exchange rate from Cathay Bank website...")
    current_rate = fetch_exchange_rate(debug=debug)
    
    if current_rate is not None:
        exchange_rates["TWD"] = current_rate
        print(f"Using freshly fetched exchange rate: 1 USD = {current_rate} TWD")
        
        # Save the exchange rate to a file
        try:
            # Create a file with the exchange rate info
            exchange_rate_data = {
                "rates": {
                    "USD": 1.0,
                    "TWD": current_rate
                },
                "lastUpdated": exchange_rates["lastUpdated"],
                "source": exchange_rates["source"]
            }
            
            # Write to the file
            with open(exchange_rate_file, 'w', encoding='utf-8') as f:
                json.dump(exchange_rate_data, f, ensure_ascii=False, indent=2)
            
            print(f"Successfully saved exchange rate ({current_rate}) to {exchange_rate_file}")
        except Exception as e:
            print(f"Error saving exchange rate: {str(e)}")
    else:
        # If fetching fails, try to use the existing exchange rate file
        if os.path.exists(exchange_rate_file):
            try:
                with open(exchange_rate_file, 'r', encoding='utf-8') as f:
                    exchange_data = json.load(f)
                    if "rates" in exchange_data and "TWD" in exchange_data["rates"]:
                        twd_rate = exchange_data["rates"]["TWD"]
                        if isinstance(twd_rate, (int, float)) and twd_rate > 0:
                            exchange_rates["TWD"] = twd_rate
                            print(f"Using exchange rate from exchange_rate.json: 1 USD = {twd_rate} TWD")
                            
                            # Add additional information for metadata
                            exchange_rates["lastUpdated"] = exchange_data.get("lastUpdated", exchange_rates["lastUpdated"])
                            exchange_rates["source"] = exchange_data.get("source", exchange_rates["source"])
            except Exception as e:
                print(f"Error reading exchange rate file: {str(e)}")
        
        print(f"Using exchange rate: 1 USD = {exchange_rates['TWD']} TWD")
    
    return exchange_rates

def csv_to_json(csv_file, json_file, product_type, exchange_rates):
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
                    twd_in_usd = twd_price / exchange_rates['TWD']
                    diff_percent = ((twd_in_usd - usd_price) / usd_price) * 100
                    p['price_difference_percent'] = round(diff_percent, 1)
                else:
                    p['price_difference_percent'] = 0
        
        # Create complete JSON structure
        data = {
            "metadata": {
                "lastUpdated": datetime.now().isoformat(),
                "exchangeRates": {
                    "USD": exchange_rates["USD"],
                    "TWD": exchange_rates["TWD"]
                },
                "regions": regions,
                "productType": product_type,
                "totalProducts": len(products)
            },
            "products": products
        }
        
        # Add exchange rate update information if available
        if "lastUpdated" in exchange_rates:
            data["metadata"]["lastExchangeRateUpdate"] = exchange_rates["lastUpdated"]
        
        if "source" in exchange_rates:
            data["metadata"]["exchangeRateSource"] = exchange_rates["source"]
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(json_file), exist_ok=True)
        
        # Write JSON file
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully converted {csv_file} to {json_file}")
        print(f"Total products: {len(products)}")
        return True
        
    except Exception as e:
        print(f"Error converting {csv_file}: {str(e)}")
        return False

def main():
    """Main program entry point"""
    print("CSV to JSON Converter for Apple Store Scraper")
    print("=" * 50)
    
    # Check for debug mode
    debug_mode = False
    if '--debug' in sys.argv:
        debug_mode = True
        sys.argv.remove('--debug')
        print("Running in DEBUG MODE: Extra diagnostic information will be displayed")
    
    # Ensure data directory exists
    data_dir = "src/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Get exchange rates - now integrated directly in this script
    exchange_rates = get_exchange_rates(debug=debug_mode)
    
    # Convert iPhone data (use consolidated data if available, otherwise fallback to merged)
    iphone_file = "iphone_products_consolidated.csv" if os.path.exists("iphone_products_consolidated.csv") else "iphone_products_merged.csv"
    iphone_success = csv_to_json(
        iphone_file, 
        os.path.join(data_dir, "iphone_data.json"),
        "iphone",
        exchange_rates
    )
    
    # Convert iPad data (use consolidated data if available, otherwise fallback to merged)
    ipad_file = "ipad_products_consolidated.csv" if os.path.exists("ipad_products_consolidated.csv") else "ipad_products_merged.csv"
    ipad_success = csv_to_json(
        ipad_file, 
        os.path.join(data_dir, "ipad_data.json"),
        "ipad",
        exchange_rates
    )
    
    # Convert Mac data (use consolidated data if available, otherwise fallback to merged)
    mac_file = "mac_products_consolidated.csv" if os.path.exists("mac_products_consolidated.csv") else "mac_products_merged.csv"
    mac_success = csv_to_json(
        mac_file,
        os.path.join(data_dir, "mac_data.json"),
        "mac",
        exchange_rates
    )
    
    # Convert Apple Watch data (use consolidated data if available, otherwise fallback to merged)
    watch_file = "watch_products_consolidated.csv" if os.path.exists("watch_products_consolidated.csv") else "watch_products_merged.csv"
    watch_success = False
    if os.path.exists(watch_file):
        watch_success = csv_to_json(
            watch_file,
            os.path.join(data_dir, "watch_data.json"),
            "watch",
            exchange_rates
        )
    
    # Convert AirPods data (use consolidated data if available, otherwise fallback to merged)
    airpods_file = "airpods_products_consolidated.csv" if os.path.exists("airpods_products_consolidated.csv") else "airpods_products_merged.csv"
    airpods_success = False
    if os.path.exists(airpods_file):
        airpods_success = csv_to_json(
            airpods_file,
            os.path.join(data_dir, "airpods_data.json"),
            "airpods",
            exchange_rates
        )
    
    # Convert Apple TV/Home data (use consolidated data if available, otherwise fallback to merged)
    tvhome_file = "tvhome_products_consolidated.csv" if os.path.exists("tvhome_products_consolidated.csv") else "tvhome_products_merged.csv"
    tvhome_success = False
    if os.path.exists(tvhome_file):
        tvhome_success = csv_to_json(
            tvhome_file,
            os.path.join(data_dir, "tvhome_data.json"),
            "tvhome",
            exchange_rates
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
    
    if mac_success:
        index["datasets"].append({
            "type": "mac",
            "file": "mac_data.json",
            "title": "Mac Models"
        })
    
    if watch_success:
        index["datasets"].append({
            "type": "watch",
            "file": "watch_data.json",
            "title": "Apple Watch Models"
        })
    
    if airpods_success:
        index["datasets"].append({
            "type": "airpods",
            "file": "airpods_data.json",
            "title": "AirPods Models"
        })
    
    if tvhome_success:
        index["datasets"].append({
            "type": "tvhome",
            "file": "tvhome_data.json",
            "title": "Apple TV & Home Models"
        })
    
    # Write index file
    with open(os.path.join(data_dir, "index.json"), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    
    print(f"\nCreated data index file: {os.path.join(data_dir, 'index.json')}")
    
    if iphone_success or ipad_success or mac_success:
        print("\nConversion completed successfully!")
    else:
        print("\nNo data was converted!")
        sys.exit(1)

if __name__ == "__main__":
    main()