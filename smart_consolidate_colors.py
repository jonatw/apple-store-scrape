#!/usr/bin/env python3
"""
Smart color consolidation — merges products that differ only by color.

All scrapers now output a consistent format (SKU, Price_US, Price_TW, PRODUCT_NAME)
so we can use a single, simple algorithm for all product types:

1. Clean color words from product names to get a base name.
2. Group products by (base_name, price) — same product at same price = color variant.
3. Keep one row per group, record available colors and variant count.

Mac products additionally group by spec columns (Chip, Memory, Storage) when available.
"""

import pandas as pd
import re
import os
from collections import defaultdict


# ==================== COLOR DICTIONARY ====================

KNOWN_COLORS = {
    # Basic colors
    'black', 'blue', 'green', 'pink', 'yellow', 'red', 'white', 'purple',
    'orange', 'gray', 'grey', 'silver', 'gold', 'brown', 'teal', 'indigo',
    'violet', 'lime', 'cyan', 'magenta',
    # Apple-specific colors (multi-word)
    'space gray', 'space grey', 'rose gold', 'midnight', 'starlight',
    'deep purple', 'alpine green', 'sierra blue', 'graphite', 'jet black',
    'product red', 'space black', 'natural titanium', 'black titanium',
    'white titanium', 'blue titanium', 'desert titanium', 'cloud white',
    'light gold', 'sky blue', 'cosmic orange', 'deep blue', 'ultramarine',
    'lavender', 'mist blue', 'sage', 'desert', 'mist',
}

# Words that look like colors but are actually part of the product identity
IGNORED_WORDS = {
    'gb', 'tb', 'inch', 'wifi', 'wi-fi', 'cellular', 'gps', 'mm',
    'fi', 'wi', 'mini', 'plus', 'max', 'pro', 'air', 'se', 'ultra',
}


# ==================== COLOR EXTRACTION ====================

def extract_colors(product_name):
    """Extract color words from a product name."""
    if not product_name or not isinstance(product_name, str):
        return []

    name_lower = product_name.lower()
    found = []

    # Multi-word colors first (greedy, longest match first)
    multi_word = sorted([c for c in KNOWN_COLORS if ' ' in c], key=len, reverse=True)
    for color in multi_word:
        if color in name_lower:
            found.append(color)
            name_lower = name_lower.replace(color, '')

    # Single-word colors in remaining text
    words = re.findall(r'\b[a-zA-Z]+\b', name_lower)
    for word in words:
        if word in KNOWN_COLORS and word not in IGNORED_WORDS:
            found.append(word)

    return list(set(found))


def clean_product_name(name):
    """Remove color words from product name to get the base product identity."""
    if not name or not isinstance(name, str):
        return ""

    clean = name.strip()

    # Remove known colors (longest first to match multi-word colors)
    for color in sorted(KNOWN_COLORS, key=len, reverse=True):
        clean = re.sub(rf'\b{re.escape(color)}\b', '', clean, flags=re.IGNORECASE)

    # Clean up punctuation artifacts
    clean = re.sub(r'\s*-\s*$', '', clean)       # trailing dash
    clean = re.sub(r'\s*-\s*', ' ', clean)        # internal dashes -> space
    clean = re.sub(r',\s*$', '', clean)            # trailing comma
    clean = re.sub(r'\s+', ' ', clean).strip()     # collapse whitespace

    return clean if clean else name.strip()


# ==================== GROUPING ====================

def make_grouping_key(row, product_type):
    """
    Create a key for grouping products that should be consolidated.

    Products with the same key are color variants of each other.
    """
    name = row.get('PRODUCT_NAME', '')
    base_name = clean_product_name(name)
    price = row.get('Price_US', 0) or 0

    if product_type.lower() == 'mac':
        # Mac: group by specs when available (chip + memory + storage + price)
        chip = row.get('Chip', '')
        memory = row.get('Memory', '')
        storage = row.get('Storage', '')
        if chip and memory and storage:
            return f"{chip}|{memory}|{storage}|{price}"

    # Default: base product name + US price
    return f"{base_name}|{price}"


# ==================== CONSOLIDATION ====================

def consolidate(df, product_type):
    """Consolidate a DataFrame by merging color variants."""
    if df.empty:
        return df

    groups = defaultdict(list)
    for idx, row in df.iterrows():
        key = make_grouping_key(row, product_type)
        groups[key].append(row)

    consolidated = []
    for items in groups.values():
        base = items[0].to_dict()

        # Collect colors from all variants
        all_colors = []
        for item in items:
            all_colors.extend(extract_colors(item.get('PRODUCT_NAME', '')))
        unique_colors = sorted(set(c.title() for c in all_colors if len(c) > 1))

        # Mac names are already clean (built from specs in post_process_products),
        # so skip color cleaning which would damage terms like "Nano-texture".
        if product_type.lower() != 'mac':
            base['PRODUCT_NAME'] = clean_product_name(base.get('PRODUCT_NAME', ''))
        base['Available_Colors'] = ', '.join(unique_colors) if unique_colors else 'Single Option'
        base['Color_Variants'] = len(items)

        # Collect all SKU variants
        skus = [str(item.get('SKU', '')) for item in items if item.get('SKU')]
        base['SKU_Variants'] = ', '.join(sorted(set(skus)))

        consolidated.append(base)

    result = pd.DataFrame(consolidated)
    return _reorder_columns(result, product_type)


def _reorder_columns(df, product_type):
    """Reorder columns for consistent, readable output."""
    ordered = ['PRODUCT_NAME']

    # Price columns
    ordered.extend(sorted(c for c in df.columns if c.startswith('Price_')))

    # Color info
    ordered.extend(['Available_Colors', 'Color_Variants', 'SKU_Variants'])

    # Mac spec columns
    if product_type.lower() == 'mac':
        for col in ['Chip', 'CPU_Cores', 'GPU_Cores', 'Neural_Engine', 'Memory', 'Storage']:
            if col in df.columns:
                ordered.append(col)

    # SKU
    if 'SKU' in df.columns:
        ordered.append('SKU')

    # Any remaining columns
    ordered.extend(c for c in df.columns if c not in ordered)

    return df[[c for c in ordered if c in df.columns]]


# ==================== MAIN ====================

PRODUCTS = [
    ('iphone_products_merged.csv', 'iphone_products_consolidated.csv', 'iPhone'),
    ('ipad_products_merged.csv', 'ipad_products_consolidated.csv', 'iPad'),
    ('mac_products_merged.csv', 'mac_products_consolidated.csv', 'Mac'),
    ('watch_products_merged.csv', 'watch_products_consolidated.csv', 'Watch'),
    ('airpods_products_merged.csv', 'airpods_products_consolidated.csv', 'AirPods'),
    ('tvhome_products_merged.csv', 'tvhome_products_consolidated.csv', 'TV/Home'),
]


def process_product_file(input_file, output_file, product_type):
    """Process a single product file."""
    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found, skipping {product_type}")
        return False

    print(f"Processing {product_type} data from {input_file}...")
    df = pd.read_csv(input_file)

    if df.empty:
        print(f"Warning: {input_file} is empty")
        return False

    print(f"Original data: {len(df)} rows")
    result = consolidate(df, product_type)

    if result.empty:
        print("Warning: No data after consolidation")
        return False

    reduction = len(df) - len(result)
    pct = (reduction / len(df) * 100) if len(df) > 0 else 0
    print(f"Consolidated data: {len(result)} rows (reduced {reduction}, {pct:.1f}%)")

    result.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"Saved to {output_file}\n")
    return True


def main():
    print("Starting Smart Color Consolidation Process...")
    print("=" * 60)

    results = []
    for input_file, output_file, product_type in PRODUCTS:
        success = process_product_file(input_file, output_file, product_type)
        results.append((product_type, success))

    print("=" * 60)
    print("Smart Color Consolidation Completed!\n")

    for product_type, success in results:
        status = "OK" if success else "SKIP"
        print(f"  [{status}] {product_type}")

    print("\nConsolidated files:")
    for _, output_file, _ in PRODUCTS:
        if os.path.exists(output_file):
            print(f"  - {output_file}")


if __name__ == "__main__":
    main()
