#!/usr/bin/env python3
import pandas as pd
import re
import os
from collections import defaultdict

class SmartColorConsolidator:
    """
    Smart color consolidation that only merges products with identical specs but different colors
    """
    
    def __init__(self):
        self.common_colors = {
            # Basic colors
            'black', 'blue', 'green', 'pink', 'yellow', 'red', 'white', 'purple', 'orange',
            'gray', 'grey', 'silver', 'gold', 'brown', 'cyan', 'magenta',
            
            # Apple-specific colors
            'space gray', 'space grey', 'rose gold', 'midnight', 'starlight', 'deep purple',
            'alpine green', 'sierra blue', 'graphite', 'jet black', 'product red',
            
            # Watch/iPhone specific
            'natural', 'slate', 'ultra', 'ceramic', 'edition'
        }
    
    def extract_color_from_name(self, product_name):
        """Extract potential color words from product name"""
        if not product_name:
            return []
        
        name_lower = product_name.lower()
        found_colors = []
        
        # Look for known colors
        for color in self.common_colors:
            if color in name_lower:
                found_colors.append(color)
        
        # Also extract words that might be colors (usually at the end)
        words = re.findall(r'\b[a-zA-Z]+\b', product_name)
        if len(words) >= 2:
            # Last 1-2 words might be colors
            potential_colors = words[-2:]
            for word in potential_colors:
                if word.lower() not in ['gb', 'tb', 'inch', 'wifi', 'cellular', 'gps', 'mm']:
                    found_colors.append(word.lower())
        
        return list(set(found_colors))
    
    def create_grouping_key(self, row, product_type):
        """Create a key for grouping products that should be consolidated"""
        
        if product_type.lower() == 'iphone':
            # For iPhone: model + storage (ignore color)
            name = row.get('PRODUCT_NAME', '')
            # Extract everything except the last word (usually color)
            parts = name.split()
            if len(parts) > 1:
                # Remove last word if it's likely a color
                last_word = parts[-1].lower()
                if last_word in self.common_colors or len(last_word) < 8:
                    base_name = ' '.join(parts[:-1])
                else:
                    base_name = name
            else:
                base_name = name
            return base_name.strip()
        
        elif product_type.lower() == 'ipad':
            # For iPad: model + storage + connectivity (ignore color after dash)
            name = row.get('PRODUCT_NAME', '')
            # Remove color part after dash
            if ' - ' in name:
                base_name = name.split(' - ')[0]
            else:
                # Try to remove color from end
                parts = name.split()
                if len(parts) > 1:
                    last_word = parts[-1].lower()
                    if last_word in self.common_colors:
                        base_name = ' '.join(parts[:-1])
                    else:
                        base_name = name
                else:
                    base_name = name
            return base_name.strip()
        
        elif product_type.lower() == 'mac':
            # For Mac: use price + chip + memory + storage as key (different configs shouldn't merge)
            price_us = row.get('Price_US', 0)
            chip = row.get('Chip', '')
            memory = row.get('Memory', '')
            storage = row.get('Storage', '')
            return f"mac_{price_us}_{chip}_{memory}_{storage}"
        
        elif product_type.lower() == 'watch':
            # For Watch: model + size + connectivity + material (ignore specific colors)
            name = row.get('PRODUCT_NAME', '')
            price_us = row.get('Price_US', 0)
            # Use price as main differentiator since different materials have different prices
            # Extract base model info
            base_parts = []
            if 'Watch' in name:
                # Extract model and size info
                parts = name.split(',')
                if len(parts) >= 2:
                    base_parts = parts[:2]  # Model and size
                    # Add connectivity if present
                    for part in parts[2:]:
                        if any(conn in part.lower() for conn in ['gps', 'cellular', 'wifi']):
                            base_parts.append(part.strip())
                            break
            
            base_name = ', '.join(base_parts) if base_parts else name
            return f"{base_name}_{price_us}"
        
        elif product_type.lower() in ['airpods', 'tvhome']:
            # For AirPods and TV/Home: use price as main differentiator
            name = row.get('PRODUCT_NAME', '')
            price_us = row.get('Price_US', 0)
            # Remove obvious color indicators
            base_name = name
            for color in self.common_colors:
                pattern = rf'\b{re.escape(color)}\b'
                base_name = re.sub(pattern, '', base_name, flags=re.IGNORECASE)
            base_name = re.sub(r'\s+', ' ', base_name).strip()
            base_name = re.sub(r'\s*-\s*$', '', base_name)  # Remove trailing dash
            return f"{base_name}_{price_us}"
        
        else:
            # Fallback: use product name + price
            name = row.get('PRODUCT_NAME', '')
            price_us = row.get('Price_US', 0)
            return f"{name}_{price_us}"
    
    def consolidate_products(self, df, product_type):
        """Consolidate products by grouping identical specs with different colors"""
        
        if df.empty:
            return df
        
        # Group by the consolidation key
        groups = defaultdict(list)
        for idx, row in df.iterrows():
            key = self.create_grouping_key(row, product_type)
            groups[key].append((idx, row))
        
        consolidated_rows = []
        
        for group_key, items in groups.items():
            if len(items) == 1:
                # Single item, no consolidation needed
                _, row = items[0]
                row_dict = row.to_dict()
                row_dict['Available_Colors'] = 'Single Option'
                row_dict['Color_Variants'] = 1
                
                # Collect SKU variants
                sku_variants = self.collect_sku_variants(items, product_type)
                row_dict.update(sku_variants)
                
                consolidated_rows.append(row_dict)
            else:
                # Multiple items, consolidate them
                consolidated_row = self.consolidate_group(items, product_type)
                consolidated_rows.append(consolidated_row)
        
        # Create DataFrame from consolidated rows
        if consolidated_rows:
            result_df = pd.DataFrame(consolidated_rows)
            # Reorder columns
            result_df = self.reorder_columns(result_df, product_type)
            return result_df
        else:
            return pd.DataFrame()
    
    def collect_sku_variants(self, items, product_type):
        """Collect SKU information from a group of items"""
        skus_us = []
        skus_tw = []
        
        for _, row in items:
            if product_type.lower() in ['iphone', 'watch']:
                # iPhone and Watch use SKU_US, SKU_TW format
                if 'SKU_US' in row and pd.notna(row['SKU_US']):
                    skus_us.append(str(row['SKU_US']))
                if 'SKU_TW' in row and pd.notna(row['SKU_TW']):
                    skus_tw.append(str(row['SKU_TW']))
            else:
                # iPad, Mac, AirPods, TV/Home use single SKU format
                if 'SKU' in row and pd.notna(row['SKU']):
                    skus_us.append(str(row['SKU']))
        
        result = {}
        if skus_us:
            if product_type.lower() in ['iphone', 'watch']:
                result['SKU_Variants_US'] = ', '.join(skus_us)
            else:
                result['SKU_Variants_US'] = ', '.join(skus_us)
        
        if skus_tw:
            result['SKU_Variants_TW'] = ', '.join(skus_tw)
        
        return result
    
    def consolidate_group(self, items, product_type):
        """Consolidate a group of similar products"""
        # Use first item as base
        _, base_row = items[0]
        result = base_row.to_dict()
        
        # Extract colors from all items
        colors = []
        all_names = []
        
        for _, row in items:
            product_name = row.get('PRODUCT_NAME', '')
            all_names.append(product_name)
            
            # Extract color from name
            extracted_colors = self.extract_color_from_name(product_name)
            colors.extend(extracted_colors)
        
        # Clean and deduplicate colors
        unique_colors = []
        for color in colors:
            color_clean = color.strip().title()
            if color_clean and color_clean not in unique_colors and len(color_clean) > 1:
                unique_colors.append(color_clean)
        
        # Set available colors
        if len(unique_colors) > 1:
            result['Available_Colors'] = ', '.join(sorted(unique_colors))
        elif len(unique_colors) == 1:
            result['Available_Colors'] = unique_colors[0]
        else:
            result['Available_Colors'] = 'Multiple Colors'
        
        result['Color_Variants'] = len(items)
        
        # Create clean product name (remove color info)
        clean_name = self.create_clean_product_name(all_names[0], product_type)
        result['PRODUCT_NAME'] = clean_name
        
        # Collect SKU variants
        sku_variants = self.collect_sku_variants(items, product_type)
        result.update(sku_variants)
        
        return result
    
    def create_clean_product_name(self, original_name, product_type):
        """Create a clean product name without color information"""
        
        if product_type.lower() == 'ipad' and ' - ' in original_name:
            # For iPad, remove everything after dash
            return original_name.split(' - ')[0]
        
        # For other products, try to remove color words from the end
        words = original_name.split()
        clean_words = []
        
        for i, word in enumerate(words):
            # Skip obvious color words, but keep technical terms
            word_lower = word.lower().strip('(),')
            if word_lower in self.common_colors and i >= len(words) - 2:
                continue  # Skip color words near the end
            clean_words.append(word)
        
        clean_name = ' '.join(clean_words)
        
        # Clean up trailing commas and spaces
        clean_name = re.sub(r',\s*$', '', clean_name)
        clean_name = re.sub(r'\s+', ' ', clean_name).strip()
        
        return clean_name if clean_name else original_name
    
    def reorder_columns(self, df, product_type):
        """Reorder columns for better readability"""
        
        base_columns = ['PRODUCT_NAME']
        
        # Add price columns
        price_columns = [col for col in df.columns if col.startswith('Price_')]
        base_columns.extend(sorted(price_columns))
        
        # Add color information
        color_columns = ['Available_Colors', 'Color_Variants']
        base_columns.extend([col for col in color_columns if col in df.columns])
        
        # Add SKU information
        sku_columns = [col for col in df.columns if 'SKU' in col]
        base_columns.extend(sorted(sku_columns))
        
        # Add product-specific columns (for Mac)
        if product_type.lower() == 'mac':
            spec_columns = ['Chip', 'CPU_Cores', 'GPU_Cores', 'Neural_Engine', 'Memory', 'Storage']
            base_columns.extend([col for col in spec_columns if col in df.columns])
        
        # Add any remaining columns
        remaining_columns = [col for col in df.columns if col not in base_columns]
        base_columns.extend(remaining_columns)
        
        # Select only existing columns
        existing_columns = [col for col in base_columns if col in df.columns]
        return df[existing_columns]

def process_product_file(input_file, output_file, product_type):
    """Process a single product file"""
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
    
    # Consolidate
    consolidator = SmartColorConsolidator()
    consolidated_df = consolidator.consolidate_products(df, product_type)
    
    if consolidated_df.empty:
        print(f"Warning: No data after consolidation")
        return False
    
    print(f"Consolidated data: {len(consolidated_df)} rows")
    reduction = len(df) - len(consolidated_df)
    reduction_pct = (reduction / len(df) * 100) if len(df) > 0 else 0
    print(f"Reduction: {reduction} rows ({reduction_pct:.1f}%)")
    
    # Save
    consolidated_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved to {output_file}")
    print()
    
    return True

def main():
    """Main function"""
    print("Starting Smart Color Consolidation Process...")
    print("=" * 60)
    
    # Process each product type
    products = [
        ('iphone_products_merged.csv', 'iphone_products_consolidated.csv', 'iPhone'),
        ('ipad_products_merged.csv', 'ipad_products_consolidated.csv', 'iPad'),
        ('mac_products_merged.csv', 'mac_products_consolidated.csv', 'Mac'),
        ('watch_products_merged.csv', 'watch_products_consolidated.csv', 'Watch'),
        ('airpods_products_merged.csv', 'airpods_products_consolidated.csv', 'AirPods'),
        ('tvhome_products_merged.csv', 'tvhome_products_consolidated.csv', 'TV/Home'),
    ]
    
    results = []
    for input_file, output_file, product_type in products:
        success = process_product_file(input_file, output_file, product_type)
        results.append((product_type, success))
    
    print("=" * 60)
    print("Smart Color Consolidation Completed!")
    print()
    
    for product_type, success in results:
        status = "✓" if success else "✗"
        print(f"{status} {product_type}")
    
    print("\nConsolidated files:")
    for _, output_file, product_type in products:
        if os.path.exists(output_file):
            print(f"  - {output_file}")

if __name__ == "__main__":
    main()