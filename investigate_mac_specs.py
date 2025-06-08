#!/usr/bin/env python3
"""
Investigation script to extract Mac specifications from Apple's website
This script explores different approaches to get detailed product specifications
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time

def investigate_json_structure(url):
    """
    Investigate the complete JSON structure from a Mac product page
    """
    print(f"\n=== Investigating JSON structure from: {url} ===")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all script tags with JSON data
    json_scripts = soup.find_all('script', {'type': 'application/json'})
    
    print(f"Found {len(json_scripts)} JSON script tags")
    
    for i, script in enumerate(json_scripts):
        script_id = script.get('id', 'no-id')
        print(f"\n--- Script {i+1} (id: {script_id}) ---")
        
        try:
            json_data = json.loads(script.string)
            
            if script_id == 'metrics':
                # This is the main product data
                data = json_data.get('data', {})
                products = data.get('products', [])
                
                print(f"Found {len(products)} products in metrics data")
                
                if products:
                    # Show detailed structure of first product
                    first_product = products[0]
                    print(f"\nDetailed structure of first product:")
                    print(json.dumps(first_product, indent=2))
                    
                    # Look for specification-related keys
                    print(f"\nAll keys in first product:")
                    for key in first_product.keys():
                        print(f"  {key}: {type(first_product[key])}")
                        
                        # If it's a dict, show its keys too
                        if isinstance(first_product[key], dict):
                            print(f"    Sub-keys: {list(first_product[key].keys())}")
            
            elif script_id and 'storefront' in script_id.lower():
                # Might contain configuration data
                print(f"Storefront data structure (first 500 chars):")
                print(json.dumps(json_data, indent=2)[:500] + "...")
                
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON in script {i+1}: {e}")
            print(f"Content preview: {script.string[:200]}...")

def investigate_html_elements(url):
    """
    Look for specification data in HTML elements (not JSON)
    """
    print(f"\n=== Investigating HTML elements from: {url} ===")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for elements that might contain specifications
    spec_indicators = [
        'spec', 'specification', 'technical', 'feature', 'memory', 'storage', 
        'processor', 'chip', 'cpu', 'gpu', 'display', 'dimension'
    ]
    
    print("Looking for specification-related elements...")
    
    for indicator in spec_indicators:
        # Look in class names
        elements = soup.find_all(attrs={'class': re.compile(indicator, re.I)})
        if elements:
            print(f"\nFound {len(elements)} elements with '{indicator}' in class:")
            for elem in elements[:3]:  # Show first 3
                print(f"  {elem.name}: {elem.get('class')} - {elem.get_text()[:100]}")
        
        # Look in data attributes
        elements = soup.find_all(attrs={re.compile(f'data.*{indicator}', re.I): True})
        if elements:
            print(f"\nFound {len(elements)} elements with '{indicator}' in data attributes:")
            for elem in elements[:3]:
                attrs = {k: v for k, v in elem.attrs.items() if indicator.lower() in k.lower()}
                print(f"  {elem.name}: {attrs}")

def investigate_api_endpoints(base_url):
    """
    Look for API endpoints that might provide detailed product information
    """
    print(f"\n=== Investigating potential API endpoints ===")
    
    # Common API patterns for Apple store
    api_patterns = [
        '/shop/product-metadata/',
        '/shop/config/',
        '/shop/product/',
        '/api/product/',
        '/services/product/',
    ]
    
    base_domain = "https://www.apple.com"
    
    for pattern in api_patterns:
        test_url = f"{base_domain}{pattern}"
        print(f"Testing: {test_url}")
        try:
            response = requests.get(test_url, timeout=5)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                if 'json' in content_type:
                    print(f"  Found JSON endpoint! Content preview:")
                    print(f"  {response.text[:200]}...")
        except Exception as e:
            print(f"  Error: {e}")

def investigate_part_numbers():
    """
    Investigate if part numbers can be used to get detailed specifications
    """
    print(f"\n=== Investigating part number lookup ===")
    
    # Sample part numbers from the previous scrape
    sample_parts = ["MWUC3LL/A", "MCX44LL/A", "MU963LL/A"]
    
    for part_number in sample_parts:
        print(f"\nTesting part number: {part_number}")
        
        # Try different URL patterns for part number lookup
        test_urls = [
            f"https://www.apple.com/shop/product/{part_number}",
            f"https://www.apple.com/shop/buy-mac/{part_number}",
            f"https://everymac.com/ultimate-mac-lookup/?search_keywords={part_number}",
        ]
        
        for url in test_urls:
            print(f"  Testing: {url}")
            try:
                response = requests.get(url, timeout=5)
                print(f"    Status: {response.status_code}")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find('title')
                    if title:
                        print(f"    Title: {title.get_text()[:100]}")
            except Exception as e:
                print(f"    Error: {e}")

def main():
    """Main investigation function"""
    print("Starting Mac specification investigation...")
    
    # Test URLs for different Mac products
    test_urls = [
        "https://www.apple.com/shop/buy-mac/imac",
        "https://www.apple.com/shop/buy-mac/mac-mini",
        "https://www.apple.com/shop/buy-mac/mac-studio",
    ]
    
    for url in test_urls:
        print(f"\n{'='*80}")
        print(f"INVESTIGATING: {url}")
        print(f"{'='*80}")
        
        # Investigate JSON structure
        investigate_json_structure(url)
        
        # Add delay between requests
        time.sleep(2)
        
        # Investigate HTML elements (only for first URL to avoid spam)
        if url == test_urls[0]:
            investigate_html_elements(url)
    
    # Investigate API endpoints
    investigate_api_endpoints("https://www.apple.com")
    
    # Investigate part number lookup
    investigate_part_numbers()

if __name__ == "__main__":
    main()