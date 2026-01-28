#!/usr/bin/env python3
"""
Comprehensive local testing before deployment
"""

import subprocess
import pandas as pd
import time
from robust_consolidation import robust_consolidate_colors

def test_product_line(product_name):
    """Test a single product line"""
    print(f"\n🧪 Testing {product_name}...")
    
    # Run the scraper (quick timeout for testing)
    try:
        cmd = f"python3 apple_scraper_manager.py run --product {product_name} --timeout 3"
        result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=300)
        
        if result.returncode != 0:
            print(f"❌ {product_name} scraper failed")
            print(result.stderr)
            return False
            
        print(f"✅ {product_name} scraper completed")
        
        # Load and analyze results
        csv_file = f"{product_name}_products_merged.csv"
        try:
            df = pd.read_csv(csv_file)
            
            # Check for color information still present
            color_count = 0
            color_examples = []
            
            for _, row in df.iterrows():
                name = str(row.get('PRODUCT_NAME', ''))
                if any(color in name.lower() for color in ['silver', 'black', 'blue', 'gold', 'space', 'midnight']):
                    color_count += 1
                    if len(color_examples) < 3:
                        color_examples.append(name)
            
            print(f"📊 {product_name}: {len(df)} products, {color_count} still have color info")
            if color_examples:
                print(f"   Examples: {color_examples}")
                
            return color_count == 0  # Success if no color info remains
            
        except FileNotFoundError:
            print(f"❌ {product_name} output file not found")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {product_name} timed out")
        return False
    except Exception as e:
        print(f"❌ {product_name} error: {e}")
        return False

def test_consolidation_logic():
    """Test the robust consolidation logic directly"""
    print(f"\n🔧 Testing robust consolidation logic...")
    
    # Create test data with color variations
    test_data = pd.DataFrame([
        {'SKU': 'A', 'Price_US': 999.0, 'Price_TW': 30000.0, 'PRODUCT_NAME': 'iPad Pro 11-inch 256GB - Silver'},
        {'SKU': 'B', 'Price_US': 999.0, 'Price_TW': 30000.0, 'PRODUCT_NAME': 'iPad Pro 11-inch 256GB - Space Black'},
        {'SKU': 'C', 'Price_US': 1299.0, 'Price_TW': 40000.0, 'PRODUCT_NAME': 'iPad Pro 11-inch 512GB - Silver'},
        {'SKU': 'D', 'Price_US': 1299.0, 'Price_TW': 40000.0, 'PRODUCT_NAME': 'iPad Pro 11-inch 512GB - Space Black'},
        {'SKU': 'E', 'Price_US': 549.0, 'Price_TW': 17990.0, 'PRODUCT_NAME': 'AirPods Max - Blue'},
    ])
    
    print(f"Test input: {len(test_data)} products")
    for _, row in test_data.iterrows():
        print(f"  {row['PRODUCT_NAME']} (${row['Price_US']})")
    
    # Apply consolidation
    result = robust_consolidate_colors(test_data, debug=True)
    
    print(f"\nTest output: {len(result)} products")
    for _, row in result.iterrows():
        print(f"  {row['PRODUCT_NAME']} (${row['Price_US']})")
    
    # Verify results
    expected_products = 3  # 2 iPad variants + 1 AirPods Max
    success = len(result) == expected_products
    
    if success:
        print(f"✅ Consolidation logic test PASSED")
    else:
        print(f"❌ Consolidation logic test FAILED - expected {expected_products}, got {len(result)}")
    
    return success

def main():
    """Run comprehensive testing"""
    print("🚀 COMPREHENSIVE LOCAL TESTING")
    print("=" * 50)
    
    # Test consolidation logic first
    logic_ok = test_consolidation_logic()
    
    if not logic_ok:
        print("\n❌ Consolidation logic failed, stopping tests")
        return False
    
    # Test each product line
    product_lines = ['airpods', 'ipad']  # Start with quick ones
    
    results = {}
    for product in product_lines:
        results[product] = test_product_line(product)
        time.sleep(2)  # Brief pause between tests
    
    # Summary
    print(f"\n📋 TEST RESULTS SUMMARY")
    print("=" * 30)
    
    all_passed = True
    for product, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{product:10s}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print(f"\n🎉 ALL TESTS PASSED - Ready for deployment!")
    else:
        print(f"\n❌ SOME TESTS FAILED - Need fixes before deployment")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)