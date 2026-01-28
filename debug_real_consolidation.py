#!/usr/bin/env python3
"""
Test consolidation logic with real iPad data
"""

import pandas as pd
import re

def test_real_consolidation():
    """Test consolidation with a subset of real iPad data"""
    
    # Real data examples that SHOULD be consolidated
    real_test_data = [
        {'SKU': 'ME2X4', 'Price_US': 1899.0, 'Price_TW': 64400.0, 'PRODUCT_NAME': '11-inch iPad Pro Wi‑Fi + Cellular 1TB with nano-texture glass - Silver'},
        {'SKU': 'ME2Y4', 'Price_US': 1899.0, 'Price_TW': 64400.0, 'PRODUCT_NAME': '11-inch iPad Pro Wi‑Fi + Cellular 1TB with nano-texture glass - Space Black'},
        
        {'SKU': 'MDEF4', 'Price_US': 1599.0, 'Price_TW': 53900.0, 'PRODUCT_NAME': '11-inch iPad Pro Wi‑Fi 1TB with standard glass - Silver'},
        {'SKU': 'MDEN4', 'Price_US': 1599.0, 'Price_TW': 53900.0, 'PRODUCT_NAME': '11-inch iPad Pro Wi‑Fi 1TB with standard glass - Space Black'},
        
        # Different storage, should not be consolidated
        {'SKU': 'MCHC4', 'Price_US': 999.0, 'Price_TW': 32900.0, 'PRODUCT_NAME': '11-inch iPad Pro Wi‑Fi 256GB with standard glass - Silver'},
        {'SKU': 'MCHD4', 'Price_US': 999.0, 'Price_TW': 32900.0, 'PRODUCT_NAME': '11-inch iPad Pro Wi‑Fi 256GB with standard glass - Space Black'},
    ]
    
    df = pd.DataFrame(real_test_data)
    print("=== REAL iPad TEST DATA ===")
    print(f"Input: {len(df)} products")
    for i, row in df.iterrows():
        print(f"  {i+1}. {row['PRODUCT_NAME']} (${row['Price_US']})")
    
    print(f"\n=== RUNNING CONSOLIDATION ===")
    consolidated = consolidate_similar_colors_debug(df)
    print(f"\nOutput: {len(consolidated)} products")
    for i, row in consolidated.iterrows():
        print(f"  {i+1}. {row['PRODUCT_NAME']} (${row['Price_US']})")
        
    print(f"\nConsolidation ratio: {len(df)} → {len(consolidated)} ({len(df)-len(consolidated)} merged)")

def consolidate_similar_colors_debug(df, price_tolerance=0.02):
    """Debug version of consolidation function with real data"""
    print(f"\n=== CONSOLIDATION DEBUG (Real Data) ===")
    
    if df.empty:
        return df
    
    # Find product name column
    product_name_col = 'PRODUCT_NAME'
    
    # Enhanced color patterns for iPad Pro
    color_patterns = [
        r'\b(space\s+black|space\s+gray|rose\s+gold|sky\s+blue|pink|blue|green|purple)\b',
        r'\b(black|white|silver|gold|gray|grey|red|yellow|orange)\b',
        r'\b(midnight|starlight|natural|graphite|jet\s+black|product\s+red)\b'
    ]
    
    def extract_base_name_and_colors(product_name):
        """Extract base model name and colors separately"""
        print(f"\n  Processing: '{product_name}'")
        if not product_name:
            return product_name, []
        
        name_lower = product_name.lower()
        found_colors = []
        original_name = name_lower
        
        # Extract colors 
        for i, pattern in enumerate(color_patterns):
            matches = re.findall(pattern, name_lower, re.IGNORECASE)
            if matches:
                print(f"    Pattern {i+1} matched: {matches}")
                found_colors.extend([m.strip().title() if isinstance(m, str) else ' '.join(m).strip().title() for m in matches])
                # Remove found colors from name
                name_lower = re.sub(pattern, ' ', name_lower, flags=re.IGNORECASE)
                print(f"    After removal: '{name_lower}'")
        
        # Enhanced cleanup for iPad Pro names
        base_name = re.sub(r'\s+', ' ', name_lower).strip()
        base_name = re.sub(r'\s*-\s*$', '', base_name)  # Remove trailing " -"
        base_name = re.sub(r'\s*-\s+$', '', base_name)  # Remove trailing "- "
        base_name = base_name.strip().title()
        
        print(f"    Final base: '{base_name}'")
        print(f"    Colors found: {found_colors}")
        return base_name, list(set(found_colors))
    
    # Process products
    df_copy = df.copy()
    base_names = []
    colors_list = []
    
    for idx, row in df_copy.iterrows():
        base_name, colors = extract_base_name_and_colors(row[product_name_col])
        base_names.append(base_name)
        colors_list.append(colors)
    
    df_copy['Base_Name'] = base_names  
    df_copy['Colors'] = colors_list
    
    print(f"\nBase names generated:")
    for base_name in set(base_names):
        count = base_names.count(base_name)
        print(f"  '{base_name}': {count} product(s)")
    
    # Group and consolidate
    consolidated_rows = []
    
    for base_name, group in df_copy.groupby('Base_Name'):
        print(f"\n--- Processing group: '{base_name}' ({len(group)} items) ---")
        
        if len(group) <= 1:
            print(f"  Single product, no consolidation needed")
            for _, row in group.iterrows():
                consolidated_rows.append(row)
        else:
            # Check prices
            print(f"  Checking prices for {len(group)} products:")
            price_cols = [col for col in group.columns if col.startswith('Price_')]
            
            should_consolidate = True
            for price_col in price_cols:
                prices = list(group[price_col].dropna())
                print(f"    {price_col}: {prices}")
                if len(prices) > 1:
                    price_range = max(prices) - min(prices)
                    avg_price = sum(prices) / len(prices)
                    diff_ratio = price_range / avg_price if avg_price > 0 else 0
                    print(f"      Range: {price_range}, Avg: {avg_price:.2f}, Ratio: {diff_ratio:.4f}")
                    if diff_ratio > price_tolerance:
                        should_consolidate = False
                        print(f"      ❌ Price difference too large ({diff_ratio:.4f} > {price_tolerance})")
                        break
                    else:
                        print(f"      ✅ Prices similar enough ({diff_ratio:.4f} <= {price_tolerance})")
            
            if should_consolidate:
                # Consolidate
                consolidated = group.iloc[0].copy()
                consolidated[product_name_col] = base_name
                print(f"  ✅ CONSOLIDATED {len(group)} products into: '{base_name}'")
                consolidated_rows.append(consolidated)
            else:
                # Keep separate
                print(f"  ❌ NOT CONSOLIDATED - keeping {len(group)} separate products")
                for _, row in group.iterrows():
                    consolidated_rows.append(row)
    
    # Return result
    result_df = pd.DataFrame(consolidated_rows)
    result_df = result_df.drop(['Base_Name', 'Colors'], axis=1, errors='ignore')
    
    return result_df

if __name__ == "__main__":
    test_real_consolidation()