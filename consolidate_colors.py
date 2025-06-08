#!/usr/bin/env python3
import pandas as pd
import re
import os

def extract_base_product_info(product_name):
    """
    Extract base product information without color
    Returns: (base_model, storage, connectivity)
    """
    # Remove color information from product name
    colors = [
        'Black', 'Blue', 'Green', 'Pink', 'Yellow', 'Red', 'White', 'Purple', 'Orange',
        'Space Gray', 'Space Grey', 'Silver', 'Gold', 'Rose Gold', 'Midnight', 'Starlight',
        'Deep Purple', 'Pro Raw', 'Alpine Green', 'Sierra Blue', 'Graphite', 'Natural Titanium',
        'Blue Titanium', 'White Titanium', 'Black Titanium'
    ]
    
    # Create pattern to match color with word boundaries and optional dashes
    color_pattern = r'\b(?:' + '|'.join(colors) + r')(?:\s+Titanium)?\b'
    
    # Remove color from product name
    base_name = re.sub(color_pattern, '', product_name, flags=re.IGNORECASE)
    
    # Clean up extra spaces and dashes
    base_name = re.sub(r'\s*-\s*$', '', base_name)  # Remove trailing dash
    base_name = re.sub(r'\s+', ' ', base_name).strip()
    
    return base_name

def collect_color_variants(group):
    """
    Collect all color variants for a product group
    """
    colors = []
    skus_us = []
    skus_tw = []
    
    for _, row in group.iterrows():
        # Extract color from product name
        product_name = row['PRODUCT_NAME']
        base_name = extract_base_product_info(product_name)
        
        # Get the color part
        color = product_name.replace(base_name, '').strip()
        color = re.sub(r'^\s*-\s*', '', color)  # Remove leading dash
        color = re.sub(r'\s*-\s*$', '', color)  # Remove trailing dash
        color = color.strip()
        
        if color:
            colors.append(color)
        
        # Collect SKUs
        if 'SKU_US' in row and pd.notna(row['SKU_US']):
            skus_us.append(str(row['SKU_US']))
        if 'SKU_TW' in row and pd.notna(row['SKU_TW']):
            skus_tw.append(str(row['SKU_TW']))
        if 'SKU' in row and pd.notna(row['SKU']):
            skus_us.append(str(row['SKU']))
    
    return {
        'available_colors': ', '.join(sorted(set(colors))) if colors else 'Multiple Colors',
        'sku_variants_us': ', '.join(skus_us) if skus_us else '',
        'sku_variants_tw': ', '.join(skus_tw) if skus_tw else '',
        'variant_count': len(group)
    }

def consolidate_product_data(input_file, output_file, product_type):
    """
    Consolidate product data by removing color variations
    """
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found, skipping {product_type}")
        return False
    
    print(f"Processing {product_type} data from {input_file}...")
    
    # Read CSV
    df = pd.read_csv(input_file)
    
    if df.empty:
        print(f"Warning: {input_file} is empty")
        return False
    
    print(f"Original data: {len(df)} rows")
    
    # Extract base product information
    df['BASE_PRODUCT'] = df['PRODUCT_NAME'].apply(extract_base_product_info)
    
    # Group by base product and price to handle same model with different prices
    if 'Price_US' in df.columns and 'Price_TW' in df.columns:
        group_columns = ['BASE_PRODUCT', 'Price_US', 'Price_TW']
    elif 'Price_US' in df.columns:
        group_columns = ['BASE_PRODUCT', 'Price_US']
    else:
        group_columns = ['BASE_PRODUCT']
    
    # Group and consolidate
    consolidated_rows = []
    
    for group_key, group in df.groupby(group_columns):
        # Get the first row as base
        base_row = group.iloc[0].copy()
        
        # Collect color variants
        color_info = collect_color_variants(group)
        
        # Update the row with consolidated information
        base_row['PRODUCT_NAME'] = base_row['BASE_PRODUCT']
        base_row['Available_Colors'] = color_info['available_colors']
        base_row['Color_Variants'] = color_info['variant_count']
        
        # Keep SKU information for reference
        if color_info['sku_variants_us']:
            base_row['SKU_Variants_US'] = color_info['sku_variants_us']
        if color_info['sku_variants_tw']:
            base_row['SKU_Variants_TW'] = color_info['sku_variants_tw']
        
        consolidated_rows.append(base_row)
    
    # Create consolidated DataFrame
    consolidated_df = pd.DataFrame(consolidated_rows)
    
    # Remove the temporary BASE_PRODUCT column
    if 'BASE_PRODUCT' in consolidated_df.columns:
        consolidated_df = consolidated_df.drop('BASE_PRODUCT', axis=1)
    
    # Reorder columns for better readability
    columns = ['PRODUCT_NAME']
    
    # Add price columns
    price_columns = [col for col in consolidated_df.columns if col.startswith('Price_')]
    columns.extend(sorted(price_columns))
    
    # Add color information
    if 'Available_Colors' in consolidated_df.columns:
        columns.append('Available_Colors')
    if 'Color_Variants' in consolidated_df.columns:
        columns.append('Color_Variants')
    
    # Add SKU information
    sku_columns = [col for col in consolidated_df.columns if col.startswith('SKU')]
    columns.extend(sorted(sku_columns))
    
    # Add any remaining columns
    remaining_columns = [col for col in consolidated_df.columns if col not in columns]
    columns.extend(remaining_columns)
    
    # Select only existing columns
    available_columns = [col for col in columns if col in consolidated_df.columns]
    consolidated_df = consolidated_df[available_columns]
    
    # Sort by product name
    consolidated_df = consolidated_df.sort_values('PRODUCT_NAME').reset_index(drop=True)
    
    # Save consolidated data
    consolidated_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    print(f"Consolidated data: {len(consolidated_df)} rows")
    print(f"Reduction: {len(df) - len(consolidated_df)} rows ({((len(df) - len(consolidated_df)) / len(df) * 100):.1f}%)")
    print(f"Saved to {output_file}")
    print()
    
    return True

def main():
    """Main function to consolidate all product data"""
    print("Starting color consolidation process...")
    print("=" * 50)
    
    # Process iPhone data
    iphone_success = consolidate_product_data(
        "iphone_products_merged.csv",
        "iphone_products_consolidated.csv",
        "iPhone"
    )
    
    # Process iPad data
    ipad_success = consolidate_product_data(
        "ipad_products_merged.csv", 
        "ipad_products_consolidated.csv",
        "iPad"
    )
    
    # Process Mac data (already consolidated, but run for consistency)
    mac_success = consolidate_product_data(
        "mac_products_merged.csv",
        "mac_products_consolidated.csv", 
        "Mac"
    )
    
    # Process AirPods data
    airpods_success = consolidate_product_data(
        "airpods_products_merged.csv",
        "airpods_products_consolidated.csv",
        "AirPods"
    )
    
    # Process Watch data
    watch_success = consolidate_product_data(
        "watch_products_merged.csv",
        "watch_products_consolidated.csv",
        "Watch"
    )
    
    # Process TV/Home data  
    tvhome_success = consolidate_product_data(
        "tvhome_products_merged.csv",
        "tvhome_products_consolidated.csv",
        "TV/Home"
    )
    
    print("=" * 50)
    print("Color consolidation completed!")
    
    if iphone_success:
        print("✓ iPhone data consolidated")
    if ipad_success:
        print("✓ iPad data consolidated") 
    if mac_success:
        print("✓ Mac data processed")
    if airpods_success:
        print("✓ AirPods data consolidated")
    if watch_success:
        print("✓ Watch data consolidated")
    if tvhome_success:
        print("✓ TV/Home data consolidated")
    
    print("\nConsolidated files:")
    expected_files = [
        "iphone_products_consolidated.csv", 
        "ipad_products_consolidated.csv", 
        "mac_products_consolidated.csv",
        "watch_products_consolidated.csv",
        "airpods_products_consolidated.csv",
        "tvhome_products_consolidated.csv"
    ]
    for file in expected_files:
        if os.path.exists(file):
            print(f"  - {file}")

if __name__ == "__main__":
    main()