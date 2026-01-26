#!/usr/bin/env python3
"""
Debug script for iPad product name extraction
"""
import requests
from bs4 import BeautifulSoup
import json
import re

def debug_ipad_page():
    """Debug a single iPad model page to see raw data structure"""
    url = "https://www.apple.com/shop/buy-ipad/ipad-air"
    print(f"Debugging URL: {url}")
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to get page: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check metrics script
        print("\n=== METRICS SCRIPT ===")
        metrics_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
        if metrics_script:
            try:
                data = json.loads(metrics_script.string)
                products = data.get('data', {}).get('products', [])
                print(f"Found {len(products)} products in metrics")
                
                if products:
                    first_product = products[0]
                    print(f"First product structure:")
                    for key, value in first_product.items():
                        if isinstance(value, str) and len(value) < 100:
                            print(f"  {key}: '{value}'")
                        elif isinstance(value, dict):
                            print(f"  {key}: {type(value).__name__} with {len(value)} keys")
                        else:
                            print(f"  {key}: {type(value).__name__}")
                            
                    # Specifically check the name field
                    name_field = first_product.get('name', '')
                    print(f"\nProduct name field: '{name_field}'")
                    
            except json.JSONDecodeError as e:
                print(f"Failed to parse metrics JSON: {e}")
        else:
            print("No metrics script found")
            
        # Check for PRODUCT_SELECTION_BOOTSTRAP
        print("\n=== BOOTSTRAP SCRIPT ===")
        bootstrap_found = False
        for script in soup.find_all('script'):
            if script.string and 'window.PRODUCT_SELECTION_BOOTSTRAP' in script.string:
                bootstrap_found = True
                print("Found bootstrap script")
                
                # Try to extract product data
                key_index = script.string.find('productSelectionData:')
                if key_index != -1:
                    print("Found productSelectionData")
                    # Extract a sample
                    sample = script.string[key_index:key_index+500]
                    print(f"Sample: {sample}")
                break
                
        if not bootstrap_found:
            print("No bootstrap script found")
            
        # Check page title as fallback
        print("\n=== PAGE TITLE ===")
        title = soup.find('title')
        if title:
            print(f"Page title: '{title.text}'")
            title_split = title.text.split('-')[0].strip()
            print(f"Title after split: '{title_split}'")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_ipad_page()