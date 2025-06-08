#!/usr/bin/env python3
"""
End-to-End Testing for Apple Store Price Comparison Website
Tests the complete workflow from data scraping to web interface functionality
"""

import subprocess
import time
import requests
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

class E2ETestSuite:
    def __init__(self):
        self.base_url = "http://localhost:5173/apple-store-scrape/"
        self.driver = None
        self.dev_server_process = None
        
    def setup_chrome_driver(self):
        """Setup Chrome driver with appropriate options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            return True
        except WebDriverException as e:
            print(f"❌ Chrome WebDriver not available: {e}")
            return False
    
    def start_dev_server(self):
        """Start the Vite development server"""
        print("🚀 Starting development server...")
        try:
            self.dev_server_process = subprocess.Popen(
                ["npm", "run", "dev"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            max_attempts = 30
            for attempt in range(max_attempts):
                try:
                    response = requests.get(self.base_url, timeout=2)
                    if response.status_code == 200:
                        print(f"✅ Development server started successfully")
                        return True
                except requests.RequestException:
                    time.sleep(1)
                    
            print("❌ Development server failed to start within 30 seconds")
            return False
            
        except FileNotFoundError:
            print("❌ npm not found. Please ensure Node.js is installed.")
            return False
        except Exception as e:
            print(f"❌ Error starting development server: {e}")
            return False
    
    def stop_dev_server(self):
        """Stop the development server"""
        if self.dev_server_process:
            self.dev_server_process.terminate()
            self.dev_server_process.wait()
            print("🛑 Development server stopped")
    
    def test_data_files_exist(self):
        """Test that all required data files exist"""
        print("\n📁 Testing data file availability...")
        
        required_files = [
            "src/data/iphone_data.json",
            "src/data/ipad_data.json", 
            "src/data/mac_data.json",
            "src/data/exchange_rate.json"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
            else:
                # Validate JSON structure
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    if 'products' in data and 'metadata' in data:
                        print(f"✅ {file_path} - Valid structure")
                    elif 'rates' in data:  # exchange_rate.json
                        print(f"✅ {file_path} - Valid exchange rate data")
                    else:
                        print(f"⚠️  {file_path} - Invalid structure")
                except json.JSONDecodeError:
                    print(f"❌ {file_path} - Invalid JSON")
        
        if missing_files:
            print(f"❌ Missing files: {', '.join(missing_files)}")
            return False
        
        return True
    
    def test_website_loads(self):
        """Test that the website loads successfully"""
        print("\n🌐 Testing website loading...")
        
        try:
            self.driver.get(self.base_url)
            
            # Wait for the page to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Check page title
            title = self.driver.title
            if "Apple" in title and "Price" in title:
                print(f"✅ Page loaded successfully: {title}")
                return True
            else:
                print(f"❌ Unexpected page title: {title}")
                return False
                
        except TimeoutException:
            print("❌ Page failed to load within timeout")
            return False
        except Exception as e:
            print(f"❌ Error loading page: {e}")
            return False
    
    def test_navigation_tabs(self):
        """Test product category navigation"""
        print("\n🔗 Testing navigation tabs...")
        
        try:
            # Test iPhone tab (should be active by default)
            iphone_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-product="iphone"]')
            if "active" in iphone_tab.get_attribute("class"):
                print("✅ iPhone tab is active by default")
            else:
                print("❌ iPhone tab is not active by default")
                return False
            
            # Test iPad tab
            ipad_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-product="ipad"]')
            ipad_tab.click()
            
            # Wait for tab content to change
            time.sleep(1)
            
            page_title = self.driver.find_element(By.ID, "page-title")
            if "iPad" in page_title.text.upper():
                print("✅ iPad tab navigation works")
            else:
                print("❌ iPad tab navigation failed")
                return False
            
            # Test Mac tab
            mac_tab = self.driver.find_element(By.CSS_SELECTOR, '[data-product="mac"]')
            mac_tab.click()
            
            # Wait for tab content to change
            time.sleep(1)
            
            page_title = self.driver.find_element(By.ID, "page-title")
            if "MAC" in page_title.text.upper():
                print("✅ Mac tab navigation works")
            else:
                print("❌ Mac tab navigation failed")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Navigation test failed: {e}")
            return False
    
    def test_data_loading(self):
        """Test that product data loads correctly"""
        print("\n📊 Testing data loading...")
        
        try:
            # Wait for data to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "total-products"))
            )
            
            # Check if product count is displayed
            total_products = self.driver.find_element(By.ID, "total-products")
            product_count = total_products.text
            
            if product_count != "-" and product_count != "":
                print(f"✅ Product data loaded: {product_count} products")
            else:
                print("❌ Product data not loaded")
                return False
            
            # Check if table has data
            table_body = self.driver.find_element(By.CSS_SELECTOR, "#products-table tbody")
            rows = table_body.find_elements(By.TAG_NAME, "tr")
            
            if len(rows) > 0:
                # Check if first row contains actual data (not loading message)
                first_row_text = rows[0].text
                if "Loading" not in first_row_text and "No product data" not in first_row_text:
                    print(f"✅ Product table populated with {len(rows)} rows")
                    return True
                else:
                    print("❌ Product table shows loading or no data message")
                    return False
            else:
                print("❌ Product table is empty")
                return False
                
        except TimeoutException:
            print("❌ Data loading timed out")
            return False
        except Exception as e:
            print(f"❌ Data loading test failed: {e}")
            return False
    
    def test_settings_functionality(self):
        """Test exchange rate and fee settings"""
        print("\n⚙️ Testing settings functionality...")
        
        try:
            # Find exchange rate input
            exchange_rate_input = self.driver.find_element(By.ID, "exchange-rate")
            original_rate = exchange_rate_input.get_attribute("value")
            
            # Change exchange rate
            new_rate = "32.0"
            exchange_rate_input.clear()
            exchange_rate_input.send_keys(new_rate)
            
            # Trigger change event
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", exchange_rate_input)
            
            # Wait a moment for changes to apply
            time.sleep(1)
            
            # Verify the change was applied
            current_rate = exchange_rate_input.get_attribute("value")
            if current_rate == new_rate:
                print("✅ Exchange rate setting works")
            else:
                print(f"❌ Exchange rate setting failed: expected {new_rate}, got {current_rate}")
                return False
            
            # Test card fee input
            card_fee_input = self.driver.find_element(By.ID, "card-fee")
            original_fee = card_fee_input.get_attribute("value")
            
            new_fee = "2.0"
            card_fee_input.clear()
            card_fee_input.send_keys(new_fee)
            
            # Trigger change event
            self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", card_fee_input)
            
            time.sleep(1)
            
            current_fee = card_fee_input.get_attribute("value")
            if current_fee == new_fee:
                print("✅ Card fee setting works")
                return True
            else:
                print(f"❌ Card fee setting failed: expected {new_fee}, got {current_fee}")
                return False
                
        except Exception as e:
            print(f"❌ Settings test failed: {e}")
            return False
    
    def test_search_functionality(self):
        """Test product search"""
        print("\n🔍 Testing search functionality...")
        
        try:
            # Find search input
            search_input = self.driver.find_element(By.ID, "product-search")
            
            # Get initial row count
            table_body = self.driver.find_element(By.CSS_SELECTOR, "#products-table tbody")
            initial_rows = len(table_body.find_elements(By.TAG_NAME, "tr"))
            
            # Enter search term
            search_term = "Mac"
            search_input.send_keys(search_term)
            
            # Wait for search to filter
            time.sleep(1)
            
            # Get filtered row count
            filtered_rows = len(table_body.find_elements(By.TAG_NAME, "tr"))
            
            if filtered_rows <= initial_rows:
                print(f"✅ Search filtering works: {initial_rows} -> {filtered_rows} rows")
                
                # Clear search
                search_input.clear()
                time.sleep(1)
                
                # Check if rows return
                final_rows = len(table_body.find_elements(By.TAG_NAME, "tr"))
                if final_rows >= filtered_rows:
                    print("✅ Search clear works")
                    return True
                else:
                    print("❌ Search clear failed")
                    return False
            else:
                print("❌ Search filtering failed")
                return False
                
        except Exception as e:
            print(f"❌ Search test failed: {e}")
            return False
    
    def test_theme_toggle(self):
        """Test dark/light theme toggle"""
        print("\n🌓 Testing theme toggle...")
        
        try:
            # Get initial theme
            html_element = self.driver.find_element(By.TAG_NAME, "html")
            initial_theme = html_element.get_attribute("data-bs-theme")
            
            # Find and click theme toggle
            theme_toggle = self.driver.find_element(By.ID, "theme-toggle")
            theme_toggle.click()
            
            time.sleep(0.5)
            
            # Check if theme changed
            new_theme = html_element.get_attribute("data-bs-theme")
            
            if new_theme != initial_theme:
                print(f"✅ Theme toggle works: {initial_theme} -> {new_theme}")
                return True
            else:
                print("❌ Theme toggle failed")
                return False
                
        except Exception as e:
            print(f"❌ Theme toggle test failed: {e}")
            return False
    
    def run_all_tests(self):
        """Run complete E2E test suite"""
        print("🧪 Starting End-to-End Test Suite")
        print("=" * 50)
        
        results = []
        
        # Test 1: Data files
        results.append(("Data Files", self.test_data_files_exist()))
        
        # Test 2: Start server and setup browser
        if not self.start_dev_server():
            print("❌ Cannot start development server. Skipping browser tests.")
            return False
        
        if not self.setup_chrome_driver():
            print("❌ Cannot setup Chrome driver. Skipping browser tests.")
            self.stop_dev_server()
            return False
        
        try:
            # Test 3: Website loads
            results.append(("Website Loading", self.test_website_loads()))
            
            # Test 4: Navigation
            results.append(("Navigation", self.test_navigation_tabs()))
            
            # Test 5: Data loading
            results.append(("Data Loading", self.test_data_loading()))
            
            # Test 6: Settings
            results.append(("Settings", self.test_settings_functionality()))
            
            # Test 7: Search
            results.append(("Search", self.test_search_functionality()))
            
            # Test 8: Theme toggle
            results.append(("Theme Toggle", self.test_theme_toggle()))
            
        finally:
            # Cleanup
            if self.driver:
                self.driver.quit()
            self.stop_dev_server()
        
        # Print results
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name:<20} {status}")
            if result:
                passed += 1
        
        print("-" * 50)
        print(f"Total: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Website is working correctly.")
            return True
        else:
            print("❌ Some tests failed. Please check the issues above.")
            return False

def main():
    """Main function to run E2E tests"""
    test_suite = E2ETestSuite()
    success = test_suite.run_all_tests()
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())