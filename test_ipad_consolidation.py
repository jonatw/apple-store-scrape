#!/usr/bin/env python3
"""
Test iPad consolidation with the actual ipad.py workflow
"""

import sys
import subprocess
import pandas as pd

def test_ipad_consolidation():
    """Test the actual iPad consolidation workflow"""
    
    print("🧪 Testing iPad consolidation workflow...")
    
    # Step 1: Load current CSV data
    try:
        df_original = pd.read_csv('ipad_products_merged.csv')
        print(f"✅ Loaded current CSV: {len(df_original)} products")
    except FileNotFoundError:
        print("❌ No existing CSV found")
        return
    
    # Step 2: Manually run consolidation on current data
    print(f"\n📊 Testing consolidation on current data...")
    
    # Import the consolidation function from ipad.py
    sys.path.append('.')
    from ipad import consolidate_similar_colors
    
    df_consolidated = consolidate_similar_colors(df_original.copy())
    print(f"📋 Consolidation result: {len(df_original)} → {len(df_consolidated)} products")
    
    if len(df_consolidated) < len(df_original):
        print(f"✅ Consolidation worked! Reduced by {len(df_original) - len(df_consolidated)} products")
        
        # Show what got consolidated
        print(f"\n🔍 Consolidated products:")
        for i, row in df_consolidated.iterrows():
            print(f"  {i+1:2d}. {row['PRODUCT_NAME']}")
    else:
        print(f"❌ No consolidation happened!")
        
        # Debug why no consolidation
        print(f"\n🔍 Analyzing why consolidation failed...")
        
        # Check for products with colors in names
        color_keywords = ['silver', 'space black', 'black', 'white', 'gold', 'gray', 'purple', 'blue', 'pink']
        
        color_products = []
        for i, row in df_original.iterrows():
            name_lower = str(row['PRODUCT_NAME']).lower()
            found_colors = [color for color in color_keywords if color in name_lower]
            if found_colors:
                color_products.append({
                    'name': row['PRODUCT_NAME'],
                    'colors': found_colors,
                    'price_us': row['Price_US'],
                    'price_tw': row['Price_TW']
                })
        
        print(f"Found {len(color_products)} products with color information:")
        for i, prod in enumerate(color_products[:10]):  # Show first 10
            print(f"  {i+1:2d}. {prod['name']} (${prod['price_us']}) - Colors: {prod['colors']}")
            
        if len(color_products) == 0:
            print("🤔 No products with color information found - this explains why no consolidation")
        else:
            print("🤔 Color products found but not consolidated - there's a bug in consolidation logic")

if __name__ == "__main__":
    test_ipad_consolidation()