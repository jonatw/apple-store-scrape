#!/usr/bin/env python3
"""
Debug consolidation logic to find root cause
"""

import pandas as pd
import re

# Test the consolidation logic with sample data
def test_consolidation():
    # Sample data similar to what we get from iPad scraper
    test_data = [
        {'SKU': 'MCFV1', 'Price_US': 599.0, 'Price_TW': 19900.0, 'PRODUCT_NAME': '11-inch iPad Air Wi-Fi 128GB - Purple'},
        {'SKU': 'MCFV2', 'Price_US': 599.0, 'Price_TW': 19900.0, 'PRODUCT_NAME': '11-inch iPad Air Wi-Fi 128GB - Blue'},
        {'SKU': 'MCFV3', 'Price_US': 599.0, 'Price_TW': 19900.0, 'PRODUCT_NAME': '11-inch iPad Air Wi-Fi 128GB - Pink'},
        {'SKU': 'MCFV4', 'Price_US': 699.0, 'Price_TW': 23900.0, 'PRODUCT_NAME': '11-inch iPad Air Wi-Fi 256GB - Purple'},
        {'SKU': 'MCFV5', 'Price_US': 699.0, 'Price_TW': 23900.0, 'PRODUCT_NAME': '11-inch iPad Air Wi-Fi 256GB - Blue'},
    ]
    
    df = pd.DataFrame(test_data)
    print("Original data:")
    print(df)
    print(f"Original rows: {len(df)}")
    
    # Run consolidation logic
    consolidated = consolidate_similar_colors(df)
    print(f"\nAfter consolidation:")
    print(consolidated)
    print(f"Consolidated rows: {len(consolidated)}")

def consolidate_similar_colors(df, price_tolerance=0.02):
    """Debug version of consolidation function"""
    print(f"\n=== CONSOLIDATION DEBUG ===")
    print(f"Input DataFrame shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    if df.empty:
        print("DataFrame is empty, returning")
        return df
    
    # Find the product name column
    product_name_col = None
    for col in df.columns:
        if 'Name_' in col or col == 'PRODUCT_NAME':
            product_name_col = col
            break
    
    print(f"Product name column: {product_name_col}")
    
    if not product_name_col:
        print("No product name column found, skipping consolidation")
        return df
    
    # Color patterns
    color_patterns = [
        r'\b(space\s+gray|rose\s+gold|sky\s+blue|pink|blue|green|purple)\b',
        r'\b(black|white|silver|gold|gray|grey|red|yellow|orange)\b',
        r'\b(midnight|starlight|natural|graphite|jet\s+black|product\s+red)\b'
    ]
    
    def extract_base_name_and_colors(product_name):
        """Extract base model name and colors separately"""
        print(f"  Processing: '{product_name}'")
        if not product_name:
            return product_name, []
        
        name_lower = product_name.lower()
        found_colors = []
        
        # Extract colors (longest patterns first)
        for i, pattern in enumerate(color_patterns):
            matches = re.findall(pattern, name_lower, re.IGNORECASE)
            if matches:
                print(f"    Pattern {i+1} matched: {matches}")
                found_colors.extend([m.strip().title() if isinstance(m, str) else ' '.join(m).strip().title() for m in matches])
                # Remove found colors from name
                name_lower = re.sub(pattern, ' ', name_lower, flags=re.IGNORECASE)
                print(f"    After removal: '{name_lower}'")
        
        # Clean up base name
        base_name = re.sub(r'\s+', ' ', name_lower).strip()
        base_name = re.sub(r'\s*-\s*$', '', base_name)
        base_name = re.sub(r'\s*-\s+$', '', base_name)
        base_name = base_name.strip().title()
        
        print(f"    Final base: '{base_name}', Colors: {found_colors}")
        return base_name, list(set(found_colors))
    
    # Process each product
    df_copy = df.copy()
    base_names = []
    colors_list = []
    
    print(f"\nProcessing {len(df_copy)} products:")
    for idx, row in df_copy.iterrows():
        base_name, colors = extract_base_name_and_colors(row[product_name_col])
        base_names.append(base_name)
        colors_list.append(colors)
    
    df_copy['Base_Name'] = base_names
    df_copy['Colors'] = colors_list
    
    print(f"\nBase names found: {set(base_names)}")
    
    # Group by base name and consolidate
    consolidated_rows = []
    
    for base_name, group in df_copy.groupby('Base_Name'):
        print(f"\nGroup '{base_name}': {len(group)} products")
        if len(group) <= 1:
            print(f"  Single product, keeping as-is")
            for _, row in group.iterrows():
                consolidated_rows.append(row)
        else:
            print(f"  Multiple products found, checking prices...")
            # Check price similarity
            price_cols = [col for col in group.columns if col.startswith('Price_')]
            
            should_consolidate = True
            for price_col in price_cols:
                prices = group[price_col].dropna()
                if len(prices) > 1:
                    price_range = max(prices) - min(prices)
                    avg_price = sum(prices) / len(prices)
                    price_diff_ratio = price_range / avg_price if avg_price > 0 else 0
                    print(f"    {price_col}: prices {list(prices)}, range={price_range:.2f}, avg={avg_price:.2f}, ratio={price_diff_ratio:.4f}")
                    if price_diff_ratio > price_tolerance:
                        should_consolidate = False
                        print(f"    Price difference too large ({price_diff_ratio:.4f} > {price_tolerance})")
                        break
            
            if should_consolidate and len(group) > 1:
                # Consolidate
                consolidated = group.iloc[0].copy()
                consolidated[product_name_col] = base_name
                print(f"  ✅ CONSOLIDATED {len(group)} variants into '{base_name}'")
                consolidated_rows.append(consolidated)
            else:
                # Don't consolidate
                print(f"  ❌ NOT CONSOLIDATED - keeping separate")
                for _, row in group.iterrows():
                    consolidated_rows.append(row)
    
    # Create result DataFrame
    result_df = pd.DataFrame(consolidated_rows)
    result_df = result_df.drop(['Base_Name', 'Colors'], axis=1, errors='ignore')
    
    return result_df

if __name__ == "__main__":
    test_consolidation()