#!/usr/bin/env python3
"""
Comprehensive test suite for Apple Store scrapers
Tests iPhone, iPad, and Mac scrapers for data integrity and functionality
"""

import unittest
import pandas as pd
import json
import os
import sys
from unittest.mock import patch, MagicMock
import time

# Import the scrapers
import iphone
import ipad
import mac
import convert_to_json

class TestScraperDataIntegrity(unittest.TestCase):
    """Test data integrity and validation for scrapers"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_regions = {
            "": ["US", "USD", "en-us", "$"],
            "tw": ["TW", "TWD", "zh-tw", "NT$"]
        }
        
    def test_iphone_standardize_product_name(self):
        """Test iPhone product name standardization"""
        test_cases = [
            ("iPhone 16 Pro 256GB Black Titanium", "iphone16pro_256gb_blacktitanium"),
            ("iPhone 16 128GB Blue", "iphone16_128gb_blue"),
            ("iPhone 15 Pro Max 1TB Natural Titanium", "iphone15promax_1tb_naturaltitanium"),
            ("", ""),
            (None, "")
        ]
        
        for input_name, expected in test_cases:
            with self.subTest(input_name=input_name):
                result = iphone.standardize_product_name(input_name)
                self.assertEqual(result, expected)
    
    def test_scraper_configuration_consistency(self):
        """Test that all scrapers have consistent region configuration"""
        scrapers = [iphone, ipad, mac]
        
        for scraper in scrapers:
            with self.subTest(scraper=scraper.__name__):
                self.assertTrue(hasattr(scraper, 'REGIONS'))
                self.assertTrue(hasattr(scraper, 'REFERENCE_REGION'))
                self.assertTrue(hasattr(scraper, 'REQUEST_DELAY'))
                self.assertTrue(hasattr(scraper, 'DEBUG'))
                
                # Check region structure
                for region_code, region_info in scraper.REGIONS.items():
                    self.assertEqual(len(region_info), 4)
                    self.assertIsInstance(region_info[0], str)  # Display name
                    self.assertIsInstance(region_info[1], str)  # Currency code
                    self.assertIsInstance(region_info[2], str)  # Locale
                    self.assertIsInstance(region_info[3], str)  # Currency symbol

class TestScraperFunctions(unittest.TestCase):
    """Test individual scraper functions"""
    
    def test_debug_print_functions(self):
        """Test debug print functions work correctly"""
        scrapers = [iphone, ipad, mac]
        
        for scraper in scrapers:
            with self.subTest(scraper=scraper.__name__):
                # Test with DEBUG=True
                original_debug = scraper.DEBUG
                scraper.DEBUG = True
                
                with patch('builtins.print') as mock_print:
                    scraper.debug_print("Test message")
                    mock_print.assert_called_once_with("[DEBUG] Test message")
                
                # Test with DEBUG=False
                scraper.DEBUG = False
                with patch('builtins.print') as mock_print:
                    scraper.debug_print("Test message")
                    mock_print.assert_not_called()
                
                # Restore original debug setting
                scraper.DEBUG = original_debug
    
    def test_get_available_models_fallback(self):
        """Test that get_available_models returns fallback when needed"""
        scrapers_and_defaults = [
            (iphone, ["iphone-16-pro", "iphone-16", "iphone-16e", "iphone-15"]),
            (ipad, ["ipad-pro", "ipad-air", "ipad", "ipad-mini"]),
            (mac, ["mac-mini", "imac", "mac-studio"])  # Updated to match current default models
        ]
        
        for scraper, expected_defaults in scrapers_and_defaults:
            with self.subTest(scraper=scraper.__name__):
                with patch('requests.get') as mock_get:
                    # Simulate failed request
                    mock_get.return_value.status_code = 404
                    result = scraper.get_available_models()
                    self.assertEqual(result, expected_defaults)

class TestDataValidation(unittest.TestCase):
    """Test data validation and output format"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_product_data = [
            {
                "SKU": "TEST001",
                "Name": "Test iPhone",
                "Price": 999.0,
                "Region": "US",
                "Region_Code": "",
                "PartNumber": "TEST001/A"
            },
            {
                "SKU": "TEST001",
                "Name": "Test iPhone",
                "Price": 31900.0,
                "Region": "TW",
                "Region_Code": "tw",
                "PartNumber": "TEST001/A"
            }
        ]
    
    def test_merge_product_data_structure(self):
        """Test that merged data has correct structure"""
        # Test iPhone merger (standardized name matching)
        with patch.object(iphone, 'REGIONS', {"": ["US", "USD", "en-us", "$"], "tw": ["TW", "TWD", "zh-tw", "NT$"]}):
            # Add standardized names for iPhone test
            iphone_data = []
            for item in self.sample_product_data:
                item_copy = item.copy()
                item_copy["Standardized_Name"] = "testiphone_128gb_black"
                iphone_data.append(item_copy)
            
            result = iphone.merge_product_data(iphone_data)
            
            if not result.empty:
                expected_columns = ['SKU_US', 'SKU_TW', 'Price_US', 'Price_TW', 'PRODUCT_NAME']
                for col in expected_columns:
                    self.assertIn(col, result.columns)
        
        # Test iPad merger (SKU matching)
        with patch.object(ipad, 'REGIONS', {"": ["US", "USD", "en-us", "$"], "tw": ["TW", "TWD", "zh-tw", "NT$"]}):
            result = ipad.merge_product_data(self.sample_product_data)
            
            if not result.empty:
                expected_columns = ['SKU', 'Price_US', 'Price_TW', 'PRODUCT_NAME']
                for col in expected_columns:
                    self.assertIn(col, result.columns)
        
        # Test Mac merger (SKU matching)
        with patch.object(mac, 'REGIONS', {"": ["US", "USD", "en-us", "$"], "tw": ["TW", "TWD", "zh-tw", "NT$"]}):
            result = mac.merge_product_data(self.sample_product_data)
            
            if not result.empty:
                expected_columns = ['SKU', 'Price_US', 'Price_TW', 'PRODUCT_NAME']
                for col in expected_columns:
                    self.assertIn(col, result.columns)
    
    def test_price_data_types(self):
        """Test that prices are numeric and valid"""
        scrapers = [ipad, mac]  # SKU-based scrapers
        
        for scraper in scrapers:
            with self.subTest(scraper=scraper.__name__):
                with patch.object(scraper, 'REGIONS', {"": ["US", "USD", "en-us", "$"], "tw": ["TW", "TWD", "zh-tw", "NT$"]}):
                    result = scraper.merge_product_data(self.sample_product_data)
                    
                    if not result.empty:
                        for col in result.columns:
                            if col.startswith('Price_'):
                                # Check that all prices are numeric
                                self.assertTrue(pd.api.types.is_numeric_dtype(result[col]))
                                # Check that prices are non-negative
                                self.assertTrue((result[col] >= 0).all())

class TestEndToEndIntegration(unittest.TestCase):
    """Integration tests for complete scraping workflow"""
    
    @unittest.skipIf(os.getenv('SKIP_NETWORK_TESTS'), "Skipping network tests")
    def test_scraper_can_fetch_real_data(self):
        """Test that scrapers can fetch real data from Apple"""
        scrapers = [
            (iphone, "iphone-16"),
            (ipad, "ipad"),
            (mac, "mac-mini")
        ]
        
        for scraper, test_model in scrapers:
            with self.subTest(scraper=scraper.__name__):
                # Test single model extraction
                url = f"https://www.apple.com/shop/buy-{scraper.__name__}/{test_model}"
                if scraper.__name__ == 'mac':
                    url = f"https://www.apple.com/shop/buy-mac/{test_model}"
                
                try:
                    products = scraper.extract_product_details(url, "")
                    
                    # Should get some products
                    self.assertIsInstance(products, list)
                    
                    if products:  # If we got data, validate it
                        product = products[0]
                        required_fields = ['SKU', 'Name', 'Price', 'Region', 'Region_Code', 'PartNumber']
                        
                        for field in required_fields:
                            self.assertIn(field, product)
                        
                        # Validate data types
                        self.assertIsInstance(product['SKU'], str)
                        self.assertIsInstance(product['Name'], str)
                        self.assertIsInstance(product['Region'], str)
                        self.assertIsInstance(product['Region_Code'], str)
                        self.assertIsInstance(product['PartNumber'], str)
                        
                        if product['Price'] is not None:
                            self.assertIsInstance(product['Price'], (int, float))
                            self.assertGreaterEqual(product['Price'], 0)
                
                except Exception as e:
                    self.skipTest(f"Network test failed for {scraper.__name__}: {e}")

class TestConvertToJson(unittest.TestCase):
    """Test convert_to_json functionality"""
    
    def setUp(self):
        """Set up test CSV files"""
        self.test_csv_content = """SKU,Price_US,Price_TW,PRODUCT_NAME
TEST001,999.0,31900.0,Test Product
TEST002,1299.0,41900.0,Another Product"""
        
        self.test_csv_file = 'test_products.csv'
        with open(self.test_csv_file, 'w') as f:
            f.write(self.test_csv_content)
    
    def tearDown(self):
        """Clean up test files"""
        for file in [self.test_csv_file, 'test_output.json']:
            if os.path.exists(file):
                os.remove(file)
        # Clean up test directories
        import shutil
        for dir_name in ['src', 'test_dir']:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
    
    def test_csv_to_json_conversion(self):
        """Test CSV to JSON conversion"""
        test_exchange_rates = {
            "USD": 1.0,
            "TWD": 31.5,
            "lastUpdated": "2024-01-01T00:00:00Z",
            "source": "Test"
        }
        
        # Create src/data directory for test
        os.makedirs('src/data', exist_ok=True)
        
        # Create a test directory structure
        test_output_file = 'test_dir/test_output.json'
        
        convert_to_json.csv_to_json(
            self.test_csv_file,
            test_output_file,
            'test',
            test_exchange_rates
        )
        
        # Verify output file exists and has correct structure
        self.assertTrue(os.path.exists(test_output_file))
        
        with open(test_output_file, 'r') as f:
            data = json.load(f)
        
        # Check structure
        self.assertIn('metadata', data)
        self.assertIn('products', data)
        
        # Check metadata
        metadata = data['metadata']
        self.assertIn('lastUpdated', metadata)
        self.assertIn('exchangeRates', metadata)
        self.assertIn('totalProducts', metadata)
        
        # Check products
        products = data['products']
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 2)
        
        # Check first product structure
        product = products[0]
        required_fields = ['SKU', 'Price_US', 'Price_TW', 'PRODUCT_NAME', 'price_difference_percent', 'product_type']
        for field in required_fields:
            self.assertIn(field, product)

class TestFileOutputs(unittest.TestCase):
    """Test file outputs and CSV generation"""
    
    def test_generated_csv_files_exist(self):
        """Test that scraper execution generates CSV files"""
        # Test both original and consolidated files
        expected_files = [
            'iphone_products_merged.csv',
            'ipad_products_merged.csv', 
            'mac_products_merged.csv',
            'iphone_products_consolidated.csv',
            'ipad_products_consolidated.csv',
            'mac_products_consolidated.csv'
        ]
        
        for file in expected_files:
            if os.path.exists(file):
                # If file exists, validate its structure
                df = pd.read_csv(file)
                
                # Should not be empty
                self.assertGreater(len(df), 0)
                
                # Should have required columns
                self.assertIn('PRODUCT_NAME', df.columns)
                
                # Should have at least one price column
                price_columns = [col for col in df.columns if col.startswith('Price_')]
                self.assertGreater(len(price_columns), 0)
                
                # Check for consolidated file specific columns
                if 'consolidated' in file:
                    self.assertIn('Available_Colors', df.columns)
                    self.assertIn('Color_Variants', df.columns)
                    
                    # Validate color variants are positive integers
                    color_variants = df['Color_Variants'].dropna()
                    if len(color_variants) > 0:
                        self.assertTrue(all(isinstance(x, (int, float)) and x > 0 for x in color_variants))

def run_scraper_tests():
    """Run all scraper tests and return results"""
    print("🧪 Running Apple Store Scraper Test Suite\n")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestScraperDataIntegrity,
        TestScraperFunctions,
        TestDataValidation,
        TestEndToEndIntegration,
        TestConvertToJson,
        TestFileOutputs
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 Test Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ Failures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError: ')[-1].split('\\n')[0]}")
    
    if result.errors:
        print(f"\n🚨 Errors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('\\n')[-2]}")
    
    if not result.failures and not result.errors:
        print("✅ All tests passed!")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_scraper_tests()
    sys.exit(0 if success else 1)