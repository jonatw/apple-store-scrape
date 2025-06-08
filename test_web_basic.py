#!/usr/bin/env python3
"""
Basic Web Test for Apple Store Price Comparison
Tests data availability and web file structure without browser automation
"""

import json
import os
import subprocess
import time
import requests

def test_data_files():
    """Test that all required data files exist and are valid"""
    print("📁 Testing data file availability...")
    
    required_files = [
        "src/data/iphone_data.json",
        "src/data/ipad_data.json", 
        "src/data/mac_data.json",
        "src/data/exchange_rate.json"
    ]
    
    results = []
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} - Missing")
            results.append(False)
        else:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if file_path.endswith('exchange_rate.json'):
                    if 'rates' in data and 'USD' in data['rates'] and 'TWD' in data['rates']:
                        print(f"✅ {file_path} - Valid exchange rate data")
                        results.append(True)
                    else:
                        print(f"❌ {file_path} - Invalid exchange rate structure")
                        results.append(False)
                else:
                    if 'products' in data and 'metadata' in data:
                        product_count = len(data['products'])
                        product_type = data['metadata'].get('productType', 'unknown')
                        print(f"✅ {file_path} - Valid structure ({product_count} {product_type} products)")
                        results.append(True)
                    else:
                        print(f"❌ {file_path} - Invalid structure")
                        results.append(False)
                        
            except json.JSONDecodeError as e:
                print(f"❌ {file_path} - Invalid JSON: {e}")
                results.append(False)
            except Exception as e:
                print(f"❌ {file_path} - Error: {e}")
                results.append(False)
    
    return all(results)

def test_web_files():
    """Test that web files exist and have basic content"""
    print("\n🌐 Testing web file structure...")
    
    required_web_files = [
        "src/index.html",
        "src/main.js",
        "src/manifest.json"
    ]
    
    results = []
    
    for file_path in required_web_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} - Missing")
            results.append(False)
        else:
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                
                if file_path.endswith('.html'):
                    if 'Apple' in content and 'Price' in content and 'data-product="mac"' in content:
                        print(f"✅ {file_path} - Valid HTML with Mac support")
                        results.append(True)
                    else:
                        print(f"❌ {file_path} - Missing Mac support or basic content")
                        results.append(False)
                        
                elif file_path.endswith('.js'):
                    if 'mac' in content and 'loadProductData' in content:
                        print(f"✅ {file_path} - Valid JavaScript with Mac support")
                        results.append(True)
                    else:
                        print(f"❌ {file_path} - Missing Mac support or core functions")
                        results.append(False)
                        
                elif file_path.endswith('.json'):
                    try:
                        json.loads(content)
                        print(f"✅ {file_path} - Valid JSON")
                        results.append(True)
                    except json.JSONDecodeError:
                        print(f"❌ {file_path} - Invalid JSON")
                        results.append(False)
                        
            except Exception as e:
                print(f"❌ {file_path} - Error reading file: {e}")
                results.append(False)
    
    return all(results)

def test_build_system():
    """Test that the build system can build the project"""
    print("\n🔧 Testing build system...")
    
    try:
        # Check if package.json has required scripts
        with open('package.json', 'r') as f:
            package_data = json.load(f)
        
        required_scripts = ['dev', 'build', 'preview']
        scripts = package_data.get('scripts', {})
        
        missing_scripts = [script for script in required_scripts if script not in scripts]
        if missing_scripts:
            print(f"❌ Missing npm scripts: {missing_scripts}")
            return False
        else:
            print("✅ All required npm scripts present")
        
        # Test build (but don't wait for completion)
        print("🔨 Testing build command...")
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Build successful")
            
            # Check if dist directory was created
            if os.path.exists('dist'):
                dist_files = os.listdir('dist')
                if len(dist_files) > 0:
                    print(f"✅ Build output created ({len(dist_files)} files in dist/)")
                    return True
                else:
                    print("❌ Build output directory is empty")
                    return False
            else:
                print("❌ Build output directory not created")
                return False
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Build timed out after 30 seconds")
        return False
    except FileNotFoundError:
        print("❌ npm not found - Node.js may not be installed")
        return False
    except Exception as e:
        print(f"❌ Build test failed: {e}")
        return False

def test_mac_data_integration():
    """Test that Mac data is properly integrated"""
    print("\n💻 Testing Mac data integration...")
    
    try:
        # Check Mac data file
        if not os.path.exists('src/data/mac_data.json'):
            print("❌ Mac data file missing")
            return False
        
        with open('src/data/mac_data.json', 'r') as f:
            mac_data = json.load(f)
        
        # Validate Mac data structure
        if 'products' not in mac_data or 'metadata' not in mac_data:
            print("❌ Mac data has invalid structure")
            return False
        
        products = mac_data['products']
        metadata = mac_data['metadata']
        
        if len(products) == 0:
            print("❌ Mac data has no products")
            return False
        
        # Check product structure
        first_product = products[0]
        required_fields = ['PRODUCT_NAME', 'Price_US', 'Price_TW']
        missing_fields = [field for field in required_fields if field not in first_product]
        
        if missing_fields:
            print(f"❌ Mac products missing fields: {missing_fields}")
            return False
        
        # Check for Mac-specific products
        mac_keywords = ['Mac', 'MacBook', 'iMac', 'Studio', 'Display']
        mac_products = [p for p in products if any(keyword in p['PRODUCT_NAME'] for keyword in mac_keywords)]
        
        if len(mac_products) == 0:
            print("❌ No Mac products found in data")
            return False
        
        print(f"✅ Mac data valid: {len(products)} products, {len(mac_products)} Mac products")
        print(f"   Sample products: {', '.join([p['PRODUCT_NAME'][:30] + '...' for p in mac_products[:3]])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mac data integration test failed: {e}")
        return False

def run_all_tests():
    """Run all basic web tests"""
    print("🧪 Starting Basic Web Test Suite")
    print("=" * 50)
    
    tests = [
        ("Data Files", test_data_files),
        ("Web Files", test_web_files),
        ("Mac Data Integration", test_mac_data_integration),
        ("Build System", test_build_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Print results summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Total: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("🎉 All tests passed! Website is ready with Mac support.")
        return True
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)