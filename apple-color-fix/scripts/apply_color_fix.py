#!/usr/bin/env python3
"""
Apply systematic color consolidation fix to all Apple product scrapers
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def apply_fix_to_product(product_type):
    """Apply robust consolidation to a specific product type"""
    
    print(f"🔧 Fixing {product_type}...")
    
    try:
        # Re-run the scraper with fixed consolidation
        script_file = f"{product_type}.py"
        if not Path(script_file).exists():
            print(f"   ❌ {script_file} not found")
            return False
            
        # Run the scraper
        result = subprocess.run(
            [sys.executable, script_file],
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            print(f"   ✅ {product_type} scraper completed successfully")
            
            # Check if consolidation worked
            csv_file = f"{product_type}_products_merged.csv"
            if Path(csv_file).exists():
                with open(csv_file, 'r') as f:
                    lines = f.readlines()
                    product_count = len(lines) - 1  # Exclude header
                    print(f"   📊 Generated {product_count} products")
            return True
        else:
            print(f"   ❌ {product_type} scraper failed:")
            print(f"      {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {product_type} scraper timed out")
        return False
    except Exception as e:
        print(f"   ❌ Error fixing {product_type}: {e}")
        return False

def verify_robust_consolidation():
    """Verify robust_consolidation.py is working correctly"""
    
    print("🧪 Testing robust consolidation logic...")
    
    try:
        # Add parent directory to path for importing
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
        
        # Test with actual iPhone data
        import pandas as pd
        from robust_consolidation import robust_consolidate_colors
        
        # Use real CSV data for testing
        try:
            test_data = pd.read_csv('iphone_products_merged.csv')
            # Filter to color variants only for testing
            color_variants = test_data[test_data['PRODUCT_NAME'].str.contains('Teal|Pink|Ultramarine', na=False)]
            if len(color_variants) == 0:
                # Fallback to sample data if no color variants found
                test_data = pd.DataFrame([
                    {'PRODUCT_NAME': 'iPhone 16 128GB Pink', 'Price_US': 729, 'Price_TW': 25900},
                    {'PRODUCT_NAME': 'iPhone 16 128GB Teal', 'Price_US': 729, 'Price_TW': 25900},
                    {'PRODUCT_NAME': 'iPhone 16 256GB Pink', 'Price_US': 829, 'Price_TW': 28900},
                ])
        except FileNotFoundError:
            # Fallback to sample data
            test_data = pd.DataFrame([
                {'PRODUCT_NAME': 'iPhone 16 128GB Pink', 'Price_US': 729, 'Price_TW': 25900},
                {'PRODUCT_NAME': 'iPhone 16 128GB Teal', 'Price_US': 729, 'Price_TW': 25900},
                {'PRODUCT_NAME': 'iPhone 16 256GB Pink', 'Price_US': 829, 'Price_TW': 28900},
            ])
        
        result = robust_consolidate_colors(test_data, debug=False)
        
        expected_consolidation = len(test_data) > len(result)
        has_clean_names = not any('Pink' in str(name) or 'Teal' in str(name) 
                                 for name in result['PRODUCT_NAME'] if pd.notna(name))
        
        if expected_consolidation and has_clean_names:
            print("   ✅ Robust consolidation is working correctly")
            return True
        else:
            print("   ❌ Robust consolidation is not working as expected")
            print(f"      Input: {len(test_data)} products")
            print(f"      Output: {len(result)} products")
            for name in result['PRODUCT_NAME']:
                print(f"        - {name}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing consolidation: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Apply color consolidation fixes')
    parser.add_argument('--product', choices=['iphone', 'ipad', 'mac', 'airpods', 'watch', 'tvhome'], 
                       help='Specific product type to fix')
    parser.add_argument('--all-products', action='store_true', 
                       help='Fix all product types')
    parser.add_argument('--test-only', action='store_true',
                       help='Only test consolidation logic, do not re-run scrapers')
    args = parser.parse_args()
    
    if not args.product and not args.all_products:
        parser.error("Must specify --product or --all-products")
    
    print("🛠️  APPLE COLOR CONSOLIDATION FIX")
    print("=" * 40)
    
    # Test consolidation logic first
    if not verify_robust_consolidation():
        print("\n❌ Consolidation logic test failed. Fix robust_consolidation.py first.")
        sys.exit(1)
    
    if args.test_only:
        print("\n✅ Test completed successfully!")
        return
    
    # Apply fixes
    product_types = ['iphone', 'ipad', 'mac', 'airpods', 'watch', 'tvhome'] if args.all_products else [args.product]
    
    results = {}
    for product_type in product_types:
        results[product_type] = apply_fix_to_product(product_type)
    
    # Summary
    print(f"\n📋 RESULTS SUMMARY")
    print("=" * 20)
    
    success_count = sum(results.values())
    total_count = len(results)
    
    for product_type, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{product_type:10s}: {status}")
    
    print(f"\nOverall: {success_count}/{total_count} products fixed successfully")
    
    if success_count == total_count:
        print("\n🎉 All fixes applied successfully! Ready for deployment.")
    else:
        print(f"\n⚠️  {total_count - success_count} products need manual attention.")

if __name__ == "__main__":
    main()