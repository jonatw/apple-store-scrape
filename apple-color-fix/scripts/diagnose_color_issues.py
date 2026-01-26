#!/usr/bin/env python3
"""
Systematic diagnosis of color variant consolidation issues
"""

import sys
import json
import argparse
from pathlib import Path

def analyze_product_data(product_type):
    """Analyze a product type for color issues"""
    
    try:
        # Try local CSV first, then remote JSON
        csv_file = f"{product_type}_products_merged.csv"
        json_url = f"https://jonatw.github.io/apple-store-scrape/{product_type}_data.json"
        
        if Path(csv_file).exists():
            import pandas as pd
            df = pd.read_csv(csv_file)
            products = df['PRODUCT_NAME'].tolist()
            source = "local CSV"
        else:
            import requests
            response = requests.get(json_url)
            data = response.json()
            products = [p['PRODUCT_NAME'] for p in data['products']]
            source = "remote JSON"
            
        print(f"📊 {product_type.upper()} Analysis ({source})")
        print(f"   Total products: {len(products)}")
        
        # Detect color variants
        color_keywords = [
            'pink', 'teal', 'ultramarine', 'silver', 'space black', 'gold', 
            'midnight', 'starlight', 'blue', 'green', 'purple', 'red', 'white',
            'black', 'yellow', 'orange', 'natural', 'graphite', 'rose gold',
            'sky blue', 'cosmic orange', 'deep blue', 'light gold'
        ]
        
        color_products = []
        potential_groups = {}
        
        for product in products:
            if not product or pd.isna(product):
                continue
                
            name_lower = product.lower()
            found_colors = [color for color in color_keywords if color in name_lower]
            
            if found_colors:
                color_products.append({
                    'name': product,
                    'colors': found_colors
                })
                
                # Extract base model (remove color)
                base = product
                for color in color_keywords:
                    base = base.replace(f' {color.title()}', '').replace(f' {color}', '')
                base = base.strip()
                
                if base in potential_groups:
                    potential_groups[base].append(product)
                else:
                    potential_groups[base] = [product]
        
        print(f"   Products with colors: {len(color_products)}")
        
        # Show consolidation opportunities
        consolidation_opportunities = 0
        for base, variants in potential_groups.items():
            if len(variants) > 1:
                consolidation_opportunities += len(variants) - 1
                print(f"   📝 '{base}' has {len(variants)} variants:")
                for variant in variants[:3]:  # Show first 3
                    print(f"      - {variant}")
                if len(variants) > 3:
                    print(f"      ... and {len(variants) - 3} more")
        
        print(f"   🎯 Potential savings: {consolidation_opportunities} products can be consolidated")
        
        return {
            'total': len(products),
            'with_colors': len(color_products),
            'groups': len([g for g in potential_groups.values() if len(g) > 1]),
            'savings': consolidation_opportunities
        }
        
    except Exception as e:
        print(f"❌ Error analyzing {product_type}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Diagnose color consolidation issues')
    parser.add_argument('--product', choices=['iphone', 'ipad', 'mac', 'airpods', 'watch', 'tvhome', 'all'], 
                       default='all', help='Product type to analyze')
    args = parser.parse_args()
    
    product_types = ['iphone', 'ipad', 'mac', 'airpods', 'watch', 'tvhome'] if args.product == 'all' else [args.product]
    
    print("🔍 APPLE COLOR CONSOLIDATION DIAGNOSIS")
    print("=" * 50)
    
    total_savings = 0
    for product_type in product_types:
        result = analyze_product_data(product_type)
        if result:
            total_savings += result['savings']
        print()
    
    print(f"🎯 TOTAL CONSOLIDATION OPPORTUNITY: {total_savings} products")
    
    if total_savings > 0:
        print("\n💡 RECOMMENDATION: Run 'python scripts/apply_color_fix.py --all-products'")
    else:
        print("\n✅ All products appear to be properly consolidated!")

if __name__ == "__main__":
    main()