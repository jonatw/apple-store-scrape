#!/usr/bin/env python3
"""
Data Validator for Apple Store Scraped Data
Validates the integrity and accuracy of scraped product data
"""

import pandas as pd
import json
import os
import re
from datetime import datetime, timedelta

class DataValidator:
    """Validates scraped Apple product data"""
    
    def __init__(self):
        self.validation_results = []
        self.errors = []
        self.warnings = []
    
    def log_result(self, test_name, passed, message="", severity="info"):
        """Log validation result"""
        result = {
            "test": test_name,
            "passed": passed,
            "message": message,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        self.validation_results.append(result)
        
        if not passed:
            if severity == "error":
                self.errors.append(result)
            elif severity == "warning":
                self.warnings.append(result)
    
    def validate_csv_structure(self, csv_file, product_type):
        """Validate CSV file structure"""
        if not os.path.exists(csv_file):
            self.log_result(f"{product_type}_csv_exists", False, 
                          f"CSV file {csv_file} does not exist", "error")
            return False
        
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            self.log_result(f"{product_type}_csv_readable", False, 
                          f"Cannot read CSV file: {e}", "error")
            return False
        
        # Check if DataFrame is empty
        if df.empty:
            self.log_result(f"{product_type}_csv_not_empty", False, 
                          f"CSV file {csv_file} is empty", "error")
            return False
        
        # Check required columns for consolidated data
        required_columns = ['PRODUCT_NAME', 'Price_US', 'Price_TW']
        
        # Consolidated files have additional columns
        if 'consolidated' in csv_file:
            required_columns.extend(['Available_Colors', 'Color_Variants'])
            # SKU columns may vary between original and consolidated formats
            optional_columns = ['SKU', 'SKU_US', 'SKU_TW', 'SKU_Variants_US', 'SKU_Variants_TW']
        else:
            # Original format requirements
            if product_type == 'iphone':
                required_columns.extend(['SKU_US', 'SKU_TW'])
            else:  # iPad and Mac use SKU format
                required_columns.extend(['SKU'])
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.log_result(f"{product_type}_required_columns", False, 
                          f"Missing columns: {missing_columns}", "error")
            return False
        
        self.log_result(f"{product_type}_csv_structure", True, 
                       f"CSV structure valid, {len(df)} products found")
        return True
    
    def validate_price_data(self, csv_file, product_type):
        """Validate price data in CSV"""
        if not os.path.exists(csv_file):
            return False
        
        df = pd.read_csv(csv_file)
        
        # Find price columns
        price_columns = [col for col in df.columns if col.startswith('Price_')]
        
        for col in price_columns:
            # Check for numeric data
            numeric_prices = pd.to_numeric(df[col], errors='coerce')
            non_numeric_count = numeric_prices.isna().sum()
            
            if non_numeric_count > 0:
                self.log_result(f"{product_type}_prices_numeric_{col}", False, 
                              f"{non_numeric_count} non-numeric prices in {col}", "warning")
            
            # Check for reasonable price ranges
            valid_prices = numeric_prices.dropna()
            if len(valid_prices) > 0:
                min_price = valid_prices.min()
                max_price = valid_prices.max()
                
                # Apple products should be reasonably priced
                expected_ranges = {
                    'Price_US': (99, 20000),    # $99 to $20,000
                    'Price_TW': (3000, 700000)  # NT$3,000 to NT$700,000
                }
                
                if col in expected_ranges:
                    min_expected, max_expected = expected_ranges[col]
                    
                    if min_price < min_expected or max_price > max_expected:
                        self.log_result(f"{product_type}_price_range_{col}", False, 
                                      f"Price range {min_price}-{max_price} outside expected {min_expected}-{max_expected}", 
                                      "warning")
                    else:
                        self.log_result(f"{product_type}_price_range_{col}", True, 
                                      f"Price range {min_price}-{max_price} is reasonable")
                
                # Check for zero prices (might indicate missing data)
                zero_prices = (valid_prices == 0).sum()
                if zero_prices > len(valid_prices) * 0.1:  # More than 10% zero prices
                    self.log_result(f"{product_type}_zero_prices_{col}", False, 
                                  f"{zero_prices} products have zero price in {col}", "warning")
        
        return True
    
    def validate_product_names(self, csv_file, product_type):
        """Validate product name consistency and format"""
        if not os.path.exists(csv_file):
            return False
        
        df = pd.read_csv(csv_file)
        
        # Check for empty product names
        empty_names = df['PRODUCT_NAME'].isna().sum() + (df['PRODUCT_NAME'] == '').sum()
        if empty_names > 0:
            self.log_result(f"{product_type}_product_names_not_empty", False, 
                          f"{empty_names} products have empty names", "error")
        
        # Product type specific validations
        names = df['PRODUCT_NAME'].dropna()
        
        if product_type == 'iphone':
            iphone_names = names[names.str.contains('iPhone|iphone', case=False, na=False)]
            if len(iphone_names) < len(names) * 0.8:  # At least 80% should be iPhones
                self.log_result(f"{product_type}_name_consistency", False, 
                              f"Only {len(iphone_names)}/{len(names)} products contain 'iPhone'", "warning")
        
        elif product_type == 'ipad':
            ipad_names = names[names.str.contains('iPad|ipad', case=False, na=False)]
            if len(ipad_names) < len(names) * 0.8:  # At least 80% should be iPads
                self.log_result(f"{product_type}_name_consistency", False, 
                              f"Only {len(ipad_names)}/{len(names)} products contain 'iPad'", "warning")
        
        elif product_type == 'mac':
            mac_keywords = ['Mac', 'MacBook', 'iMac', 'Studio Display', 'Pro Display']
            mac_names = names[names.str.contains('|'.join(mac_keywords), case=False, na=False)]
            if len(mac_names) < len(names) * 0.8:  # At least 80% should be Mac products
                self.log_result(f"{product_type}_name_consistency", False, 
                              f"Only {len(mac_names)}/{len(names)} products contain Mac keywords", "warning")
        
        self.log_result(f"{product_type}_product_names", True, 
                       f"Product names validated for {len(names)} products")
        return True
    
    def validate_json_output(self, json_file, product_type):
        """Validate JSON output format"""
        if not os.path.exists(json_file):
            self.log_result(f"{product_type}_json_exists", False, 
                          f"JSON file {json_file} does not exist", "error")
            return False
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.log_result(f"{product_type}_json_readable", False, 
                          f"Cannot read JSON file: {e}", "error")
            return False
        
        # Check required structure
        required_keys = ['metadata', 'products']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            self.log_result(f"{product_type}_json_structure", False, 
                          f"Missing JSON keys: {missing_keys}", "error")
            return False
        
        # Validate metadata
        metadata = data['metadata']
        required_metadata = ['lastUpdated', 'exchangeRates', 'totalProducts', 'productType']
        missing_metadata = [key for key in required_metadata if key not in metadata]
        if missing_metadata:
            self.log_result(f"{product_type}_json_metadata", False, 
                          f"Missing metadata keys: {missing_metadata}", "error")
        
        # Validate products array
        products = data['products']
        if not isinstance(products, list):
            self.log_result(f"{product_type}_json_products_array", False, 
                          "Products should be an array", "error")
            return False
        
        if len(products) == 0:
            self.log_result(f"{product_type}_json_products_not_empty", False, 
                          "Products array is empty", "error")
            return False
        
        # Validate individual product structure
        product = products[0]
        required_product_keys = ['PRODUCT_NAME', 'price_difference_percent', 'product_type']
        missing_product_keys = [key for key in required_product_keys if key not in product]
        if missing_product_keys:
            self.log_result(f"{product_type}_json_product_structure", False, 
                          f"Missing product keys: {missing_product_keys}", "warning")
        
        self.log_result(f"{product_type}_json_format", True, 
                       f"JSON format valid, {len(products)} products")
        return True
    
    def validate_exchange_rates(self):
        """Validate exchange rate data"""
        exchange_file = 'src/data/exchange_rate.json'
        
        if not os.path.exists(exchange_file):
            self.log_result("exchange_rates_exists", False, 
                          "Exchange rate file does not exist", "warning")
            return False
        
        try:
            with open(exchange_file, 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.log_result("exchange_rates_readable", False, 
                          f"Cannot read exchange rate file: {e}", "error")
            return False
        
        # Check structure
        if 'rates' not in data:
            self.log_result("exchange_rates_structure", False, 
                          "Missing 'rates' key in exchange rate data", "error")
            return False
        
        rates = data['rates']
        if 'USD' not in rates or 'TWD' not in rates:
            self.log_result("exchange_rates_currencies", False, 
                          "Missing USD or TWD in exchange rates", "error")
            return False
        
        # Check if rates are reasonable
        usd_rate = rates['USD']
        twd_rate = rates['TWD']
        
        if usd_rate != 1.0:
            self.log_result("exchange_rates_usd_base", False, 
                          f"USD rate should be 1.0, got {usd_rate}", "warning")
        
        if not (25 <= twd_rate <= 35):  # Reasonable TWD/USD range
            self.log_result("exchange_rates_twd_reasonable", False, 
                          f"TWD rate {twd_rate} seems unreasonable", "warning")
        
        # Check if rates are recent
        if 'lastUpdated' in data:
            try:
                last_updated = datetime.fromisoformat(data['lastUpdated'].replace('Z', '+00:00'))
                if datetime.now().timestamp() - last_updated.timestamp() > 7 * 24 * 3600:  # 7 days
                    self.log_result("exchange_rates_recent", False, 
                                  f"Exchange rates are older than 7 days", "warning")
                else:
                    self.log_result("exchange_rates_recent", True, 
                                  "Exchange rates are recent")
            except Exception:
                self.log_result("exchange_rates_timestamp", False, 
                              "Invalid timestamp format", "warning")
        
        self.log_result("exchange_rates_valid", True, 
                       f"Exchange rates valid: USD={usd_rate}, TWD={twd_rate}")
        return True
    
    def run_all_validations(self):
        """Run all validation tests"""
        print("🔍 Running Data Validation Tests...\n")
        
        # Test files mapping - using consolidated data files
        test_files = [
            ('iphone', 'iphone_products_consolidated.csv', 'src/data/iphone_data.json'),
            ('ipad', 'ipad_products_consolidated.csv', 'src/data/ipad_data.json'),
            ('mac', 'mac_products_consolidated.csv', 'src/data/mac_data.json')
        ]
        
        for product_type, csv_file, json_file in test_files:
            print(f"Validating {product_type.upper()} data...")
            
            # Validate CSV
            if self.validate_csv_structure(csv_file, product_type):
                self.validate_price_data(csv_file, product_type)
                self.validate_product_names(csv_file, product_type)
            
            # Validate JSON
            self.validate_json_output(json_file, product_type)
        
        # Validate exchange rates
        print("Validating exchange rates...")
        self.validate_exchange_rates()
        
        self.print_summary()
    
    def print_summary(self):
        """Print validation summary"""
        total_tests = len(self.validation_results)
        passed_tests = len([r for r in self.validation_results if r['passed']])
        
        print(f"\n📊 Validation Summary:")
        print(f"Total tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Success rate: {(passed_tests / total_tests * 100):.1f}%")
        
        if self.errors:
            print(f"\n❌ Errors:")
            for error in self.errors:
                print(f"  - {error['test']}: {error['message']}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"  - {warning['test']}: {warning['message']}")
        
        if not self.errors and not self.warnings:
            print("✅ All validations passed!")
        
        return len(self.errors) == 0

def main():
    """Main validation function"""
    validator = DataValidator()
    success = validator.run_all_validations()
    return success

if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)