#!/usr/bin/env python3
"""
Enhanced investigation script to extract detailed Mac specifications
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time

def extract_html_specifications(url):
    """
    Extract specifications from HTML elements on Mac product pages
    """
    print(f"\n=== Extracting HTML specifications from: {url} ===")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    specifications = {}
    
    # Look for specification lists
    spec_lists = soup.find_all('ul', class_=re.compile(r'.*spec.*', re.I))
    print(f"Found {len(spec_lists)} specification lists")
    
    for i, spec_list in enumerate(spec_lists):
        print(f"\nSpec list {i+1}:")
        items = spec_list.find_all('li')
        for item in items:
            text = item.get_text(strip=True)
            print(f"  - {text}")
    
    # Look for dimension/configuration elements that might contain CPU, storage, memory info
    dimension_elements = soup.find_all(attrs={'class': re.compile(r'.*dimension.*', re.I)})
    print(f"\nFound {len(dimension_elements)} dimension-related elements")
    
    for i, elem in enumerate(dimension_elements[:5]):  # Show first 5
        text = elem.get_text(strip=True)
        if text and len(text) < 200:  # Only show reasonably short text
            print(f"  Dimension {i+1}: {text}")
    
    # Look for product bundle elements
    bundle_elements = soup.find_all(attrs={'class': re.compile(r'.*productbundle.*', re.I)})
    print(f"\nFound {len(bundle_elements)} product bundle elements")
    
    for i, elem in enumerate(bundle_elements[:3]):
        text = elem.get_text(strip=True)
        if text and len(text) < 300:
            print(f"  Bundle {i+1}: {text}")
    
    return specifications

def investigate_individual_product_page(part_number):
    """
    Investigate individual product pages using part numbers
    """
    url = f"https://www.apple.com/shop/product/{part_number}"
    print(f"\n=== Investigating individual product page: {url} ===")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return {}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Look for technical specifications section
    tech_specs = soup.find_all(string=re.compile(r'technical.*spec', re.I))
    print(f"Found {len(tech_specs)} references to technical specifications")
    
    # Look for specification tables or lists
    spec_elements = soup.find_all(['table', 'dl', 'ul'], 
                                 attrs={'class': re.compile(r'.*(spec|tech).*', re.I)})
    print(f"Found {len(spec_elements)} specification tables/lists")
    
    for i, elem in enumerate(spec_elements):
        print(f"\nSpec element {i+1} ({elem.name}):")
        text = elem.get_text()[:300]  # First 300 chars
        print(f"  {text}...")
    
    # Look for JSON data that might contain detailed specs
    json_scripts = soup.find_all('script', {'type': 'application/json'})
    
    for script in json_scripts:
        script_id = script.get('id', 'no-id')
        if script_id in ['metrics', 'product-data', 'specifications']:
            print(f"\nFound JSON script: {script_id}")
            try:
                json_data = json.loads(script.string)
                print(f"  Keys: {list(json_data.keys())}")
                
                # Look for product or specification data
                if 'product' in json_data:
                    product = json_data['product']
                    print(f"  Product keys: {list(product.keys())}")
                elif 'data' in json_data:
                    data = json_data['data']
                    print(f"  Data keys: {list(data.keys())}")
                    
            except json.JSONDecodeError:
                print(f"  Failed to parse JSON")

def extract_specs_from_buy_page_html(url):
    """
    Enhanced extraction of specifications from the buy page HTML
    """
    print(f"\n=== Enhanced HTML spec extraction from: {url} ===")
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = []
    
    # Look for product configuration sections
    product_sections = soup.find_all('div', attrs={'class': re.compile(r'.*product.*', re.I)})
    
    for section in product_sections:
        # Look for configuration text within each product section
        config_text = section.get_text()
        
        # Extract specifications using regex patterns
        specs = extract_specs_from_text(config_text)
        
        if any(specs.values()):  # If we found any specs
            products.append(specs)
    
    return products

def extract_specs_from_text(text):
    """
    Extract specifications from text using regex patterns
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
    
    text_lower = text.lower()
    
    # Extract chip information (M1, M2, M3, M4)
    chip_pattern = r'(apple\s+)?(m[1-4](?:\s+(?:pro|max|ultra))?)\s+chip'
    chip_match = re.search(chip_pattern, text_lower)
    if chip_match:
        specs['chip'] = chip_match.group(2).upper()
    
    # Extract CPU cores
    cpu_pattern = r'(\d+)-core\s+cpu'
    cpu_match = re.search(cpu_pattern, text_lower)
    if cpu_match:
        specs['cpu_cores'] = f"{cpu_match.group(1)}-core CPU"
    
    # Extract GPU cores
    gpu_pattern = r'(\d+)-core\s+gpu'
    gpu_match = re.search(gpu_pattern, text_lower)
    if gpu_match:
        specs['gpu_cores'] = f"{gpu_match.group(1)}-core GPU"
    
    # Extract Neural Engine
    neural_pattern = r'(\d+)-core\s+neural\s+engine'
    neural_match = re.search(neural_pattern, text_lower)
    if neural_match:
        specs['neural_engine'] = f"{neural_match.group(1)}-core Neural Engine"
    
    # Extract memory
    memory_patterns = [
        r'(\d+)gb\s+(?:unified\s+)?memory',
        r'memory[:\s]+(\d+)gb'
    ]
    for pattern in memory_patterns:
        memory_match = re.search(pattern, text_lower)
        if memory_match:
            specs['memory'] = f"{memory_match.group(1)}GB"
            break
    
    # Extract storage
    storage_patterns = [
        r'(\d+)(gb|tb)\s+storage',
        r'storage[:\s]+(\d+)(gb|tb)'
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
            specs['display'] = f"{display_match.group(1)}-inch display"
            break
    
    return specs

def main():
    """Main enhanced investigation function"""
    print("Starting enhanced Mac specification investigation...")
    
    # Test with different Mac product pages
    test_urls = [
        "https://www.apple.com/shop/buy-mac/imac",
        "https://www.apple.com/shop/buy-mac/mac-mini",
    ]
    
    for url in test_urls:
        extract_html_specifications(url)
        extract_specs_from_buy_page_html(url)
        time.sleep(2)
    
    # Test individual product pages
    sample_part_numbers = ["MWUC3LL/A", "MCX44LL/A"]
    
    for part_number in sample_part_numbers:
        investigate_individual_product_page(part_number)
        time.sleep(2)

if __name__ == "__main__":
    main()