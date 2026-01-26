#!/usr/bin/env python3
"""
Robust consolidation logic for all Apple product lines
This will be the definitive, bulletproof solution for color consolidation
"""

import pandas as pd
import re
from typing import Tuple, List, Dict, Any

def robust_consolidate_colors(df: pd.DataFrame, 
                            price_tolerance: float = 0.02,
                            debug: bool = False) -> pd.DataFrame:
    """
    Robust color consolidation that actually works
    
    Strategy:
    1. Extract model + storage pattern (ignore everything else)
    2. Group by this pattern  
    3. If prices are similar, consolidate
    4. Use the cleanest name as the final name
    
    Args:
        df: DataFrame with PRODUCT_NAME column
        price_tolerance: Maximum price difference ratio to allow consolidation
        debug: Print debug information
        
    Returns:
        Consolidated DataFrame
    """
    if debug:
        print(f"🔧 ROBUST CONSOLIDATION: {len(df)} input products")
    
    if df.empty:
        return df
    
    # Find product name column
    product_name_col = None
    for col in df.columns:
        if col in ['PRODUCT_NAME', 'Name_US', 'Name_TW'] or 'Name_' in col:
            product_name_col = col
            break
    
    if not product_name_col:
        if debug:
            print("❌ No product name column found")
        return df
    
    if debug:
        print(f"✅ Using column: {product_name_col}")
    
    # Step 1: Extract core model pattern for each product
    df_work = df.copy()
    df_work['Core_Pattern'] = df_work[product_name_col].apply(
        lambda x: extract_core_pattern(x, debug)
    )
    
    if debug:
        print(f"\n📋 Core patterns found:")
        for pattern in sorted(df_work['Core_Pattern'].unique()):
            count = (df_work['Core_Pattern'] == pattern).sum()
            print(f"  '{pattern}': {count} product(s)")
    
    # Step 2: Group by core pattern and consolidate
    consolidated_rows = []
    
    for pattern, group in df_work.groupby('Core_Pattern'):
        if debug:
            print(f"\n🔄 Processing pattern: '{pattern}' ({len(group)} products)")
        
        if len(group) == 1:
            if debug:
                print(f"  ✅ Single product, cleaning name")
            # Even for single products, clean the name
            cleaned = group.iloc[0].copy()
            cleaned[product_name_col] = pattern  # Use the clean pattern as the name
            consolidated_rows.append(cleaned.to_dict())
        else:
            # Multiple products with same core pattern
            if should_consolidate_group(group, price_tolerance, debug):
                # Consolidate: pick the best representative name
                best_name = select_best_product_name(group[product_name_col].tolist(), debug)
                consolidated = group.iloc[0].copy()
                consolidated[product_name_col] = best_name
                
                if debug:
                    print(f"  ✅ CONSOLIDATED {len(group)} → '{best_name}'")
                consolidated_rows.append(consolidated.to_dict())
            else:
                # Don't consolidate
                if debug:
                    print(f"  ❌ NOT CONSOLIDATED - keeping {len(group)} separate")
                consolidated_rows.extend(group.to_dict('records'))
    
    # Step 3: Create result DataFrame
    result_df = pd.DataFrame(consolidated_rows)
    result_df = result_df.drop(['Core_Pattern'], axis=1, errors='ignore')
    
    if debug:
        reduction = len(df) - len(result_df)
        print(f"\n🎉 FINAL RESULT: {len(df)} → {len(result_df)} (-{reduction} products, {reduction/len(df)*100:.1f}% reduction)")
    
    return result_df

def extract_core_pattern(product_name: str, debug: bool = False) -> str:
    """
    Extract the core pattern from a product name
    
    Strategy: Keep model + storage, remove colors and minor variations
    
    Examples:
    - "11-inch iPad Pro Wi‑Fi 1TB with nano-texture glass - Silver" 
      → "11-inch iPad Pro Wi‑Fi 1TB with nano-texture glass"
    - "iPhone 17 Pro 256GB Cosmic Orange" 
      → "iPhone 17 Pro 256GB"
    """
    if not product_name or pd.isna(product_name):
        return ""
    
    name = str(product_name).strip()
    
    # Remove color suffixes (most common pattern: " - Color")
    name = re.sub(r'\s*-\s*(Silver|Space Black|Gold|Rose Gold|Pink|Blue|Green|Purple|Red|Yellow|Orange|Black|White|Gray|Grey|Midnight|Starlight|Natural|Graphite|Product Red)(\s|$)', '', name, flags=re.IGNORECASE)
    
    # Remove standalone color words at the end
    color_words = [
        'silver', 'gold', 'black', 'white', 'gray', 'grey', 'pink', 'blue', 'green', 
        'purple', 'red', 'yellow', 'orange', 'midnight', 'starlight', 'natural', 
        'graphite', 'cosmic orange', 'deep blue', 'light gold', 'cloud white', 
        'space black', 'sky blue', 'rose gold', 'product red', 'jet black',
        'space gray', 'alpine green', 'sierra blue'
    ]
    
    # Sort by length (longest first) to handle "Space Black" before "Black"
    for color in sorted(color_words, key=len, reverse=True):
        # Remove color at the end of the string
        pattern = rf'\s+{re.escape(color)}\s*$'
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)
        
        # Remove color in the middle (surrounded by spaces/dashes)
        pattern = rf'\s+{re.escape(color)}\s+'
        name = re.sub(pattern, ' ', name, flags=re.IGNORECASE)
    
    # Clean up extra spaces and dashes
    name = re.sub(r'\s+', ' ', name)  # Multiple spaces → single space
    name = re.sub(r'\s*-\s*$', '', name)  # Remove trailing dash
    name = name.strip()
    
    return name

def should_consolidate_group(group: pd.DataFrame, 
                           price_tolerance: float,
                           debug: bool = False) -> bool:
    """
    Determine if a group of products should be consolidated
    
    Criteria: All price columns must have similar values
    """
    price_cols = [col for col in group.columns if col.startswith('Price_')]
    
    for price_col in price_cols:
        prices = group[price_col].dropna()
        if len(prices) <= 1:
            continue
            
        price_range = max(prices) - min(prices)
        avg_price = sum(prices) / len(prices)
        
        if avg_price == 0:
            continue  # Skip zero prices
            
        diff_ratio = price_range / avg_price
        
        if debug:
            print(f"    {price_col}: range={price_range:.2f}, avg={avg_price:.2f}, ratio={diff_ratio:.4f}")
        
        if diff_ratio > price_tolerance:
            if debug:
                print(f"    ❌ Price difference too large ({diff_ratio:.4f} > {price_tolerance})")
            return False
    
    if debug:
        print(f"    ✅ All prices similar enough")
    return True

def select_best_product_name(names: List[str], debug: bool = False) -> str:
    """
    Select the best representative name from a group
    
    Criteria:
    1. Shortest name (least cluttered)
    2. No color suffixes
    3. Standard capitalization
    """
    if not names:
        return ""
    
    if len(names) == 1:
        return names[0]
    
    # Score each name (lower is better)
    scored_names = []
    for name in names:
        score = 0
        
        # Prefer shorter names
        score += len(name)
        
        # Penalize names with color indicators
        color_indicators = ['-', 'silver', 'black', 'gold', 'space', 'midnight']
        for indicator in color_indicators:
            if indicator.lower() in name.lower():
                score += 50
        
        scored_names.append((score, name))
    
    # Sort by score and pick the best
    scored_names.sort(key=lambda x: x[0])
    best_name = scored_names[0][1]
    
    if debug:
        print(f"    Best name selected: '{best_name}' from {len(names)} options")
    
    return best_name

def fix_ipad_consolidation():
    """Apply robust consolidation to current iPad data"""
    
    print("🔧 FIXING iPad consolidation with robust logic...")
    
    # Load current data
    try:
        df = pd.read_csv('ipad_products_merged.csv')
        print(f"✅ Loaded: {len(df)} products")
    except FileNotFoundError:
        print("❌ ipad_products_merged.csv not found")
        return
    
    # Apply robust consolidation
    df_fixed = robust_consolidate_colors(df, debug=True)
    
    # Save fixed version
    df_fixed.to_csv('ipad_products_merged.csv', index=False)
    print(f"\n💾 Saved fixed version: {len(df_fixed)} products")
    
    # Show results
    print(f"\n📋 Fixed products:")
    for i, row in df_fixed.head(10).iterrows():
        print(f"  {i+1:2d}. {row['PRODUCT_NAME']} (${row['Price_US']})")
    
    if len(df_fixed) < len(df):
        print(f"\n🎉 SUCCESS! Reduced from {len(df)} to {len(df_fixed)} products")
    else:
        print(f"\n🤔 No consolidation happened - check data")

if __name__ == "__main__":
    fix_ipad_consolidation()