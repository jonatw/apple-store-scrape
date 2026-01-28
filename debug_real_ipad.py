#!/usr/bin/env python3
"""
Debug real iPad data to find why consolidation isn't working
"""

import pandas as pd
import re
import subprocess
import sys

def debug_real_ipad_data():
    """Load real iPad data and analyze consolidation"""
    
    # Read actual CSV
    try:
        df = pd.read_csv('ipad_products_merged.csv')
        print(f"Loaded real iPad data: {len(df)} products")
        print(f"Columns: {df.columns.tolist()}")
        
        # Show sample data
        print(f"\nFirst 10 products:")
        for i, row in df.head(10).iterrows():
            print(f"  {i+1:2d}. {row['PRODUCT_NAME']} (${row['Price_US']}, NT${row['Price_TW']})")
            
        # Check if any product names contain color indicators
        color_keywords = ['purple', 'blue', 'pink', 'silver', 'gold', 'space', 'gray', 'black', 'white', 
                         'red', 'green', 'yellow', 'orange', 'midnight', 'starlight']
        
        print(f"\n=== COLOR ANALYSIS ===")
        color_found = False
        for i, row in df.iterrows():
            name_lower = str(row['PRODUCT_NAME']).lower()
            found_colors = [color for color in color_keywords if color in name_lower]
            if found_colors:
                print(f"Colors found in '{row['PRODUCT_NAME']}': {found_colors}")
                color_found = True
        
        if not color_found:
            print("❌ NO COLOR INFORMATION found in any product names!")
            print("This explains why consolidation didn't work.")
            
        # Analyze potential duplicates by similar names
        print(f"\n=== POTENTIAL DUPLICATE ANALYSIS ===")
        name_groups = {}
        for i, row in df.iterrows():
            # Extract base name by removing specific details
            name = str(row['PRODUCT_NAME']).lower()
            
            # Try to extract base model pattern
            # Example: "11-inch ipad air wi-fi 128gb" -> "11-inch ipad air wi-fi"
            base_pattern = re.sub(r'\b\d+gb\b', '[SIZE]', name)  # Replace storage size
            base_pattern = re.sub(r'\b\d+tb\b', '[SIZE]', base_pattern)  # Replace TB storage
            
            if base_pattern not in name_groups:
                name_groups[base_pattern] = []
            name_groups[base_pattern].append({
                'name': row['PRODUCT_NAME'],
                'price_us': row['Price_US'], 
                'price_tw': row['Price_TW'],
                'sku': row['SKU']
            })
        
        # Show groups with multiple items
        duplicates_found = False
        for pattern, items in name_groups.items():
            if len(items) > 1:
                print(f"\nPattern: '{pattern}' ({len(items)} items)")
                for item in items:
                    print(f"  - {item['name']} (${item['price_us']}, NT${item['price_tw']})")
                duplicates_found = True
                
        if not duplicates_found:
            print("❌ NO DUPLICATE PATTERNS found!")
            print("Each product appears to be genuinely unique.")
            
        # Final diagnosis
        print(f"\n=== DIAGNOSIS ===")
        if not color_found and not duplicates_found:
            print("🎯 ROOT CAUSE: iPad data contains no color variants!")
            print("   Each product is already a unique model+storage combination.")
            print("   No consolidation is needed or possible.")
            print("   The 76 products are genuinely 76 different configurations.")
        else:
            print("🤔 Unexpected: Found potential duplicates but consolidation didn't work.")
            print("   This suggests a bug in the consolidation logic.")
            
    except FileNotFoundError:
        print("❌ ipad_products_merged.csv not found!")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return

if __name__ == "__main__":
    debug_real_ipad_data()