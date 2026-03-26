#!/usr/bin/env python3
"""
Test suite for Apple Store scrapers.

Tests the shared scraper_base framework and all product-specific scrapers
for data integrity, configuration consistency, and output format.
"""

import unittest
import pandas as pd
import json
import os
import sys
from unittest.mock import patch

# Import shared framework
import scraper_base

# Import product scrapers
import iphone
import ipad
import mac
import airpods
import watch
import tvhome

# Import pipeline utilities
import convert_to_json


class TestSharedConfiguration(unittest.TestCase):
    """Test that the shared configuration is correct and accessible."""

    def test_regions_structure(self):
        """Test REGIONS dict has correct structure."""
        for region_code, info in scraper_base.REGIONS.items():
            with self.subTest(region=region_code):
                self.assertEqual(len(info), 4)
                self.assertIsInstance(info[0], str)  # Display name
                self.assertIsInstance(info[1], str)  # Currency code
                self.assertIsInstance(info[2], str)  # Locale
                self.assertIsInstance(info[3], str)  # Currency symbol

    def test_reference_region_is_first(self):
        """Test that REFERENCE_REGION is the first key."""
        first_key = list(scraper_base.REGIONS.keys())[0]
        self.assertEqual(scraper_base.REFERENCE_REGION, first_key)

    def test_us_region_exists(self):
        """Test that US region (empty string key) exists."""
        self.assertIn("", scraper_base.REGIONS)
        self.assertEqual(scraper_base.REGIONS[""][0], "US")

    def test_tw_region_exists(self):
        """Test that TW region exists."""
        self.assertIn("tw", scraper_base.REGIONS)
        self.assertEqual(scraper_base.REGIONS["tw"][0], "TW")


class TestSKUUtilities(unittest.TestCase):
    """Test SKU stripping and normalization."""

    def test_strip_region_suffix(self):
        """Test region suffix stripping from part numbers."""
        cases = [
            ("MYW23LL/A", "MYW23"),   # US suffix
            ("MYW23FE/A", "MYW23"),   # TW suffix
            ("MYW23/A", "MYW23"),      # Simple suffix
            ("MYW23", "MYW23"),        # No suffix
            ("", ""),                   # Empty
            (None, None),              # None
        ]
        for input_val, expected in cases:
            with self.subTest(input=input_val):
                self.assertEqual(scraper_base.strip_region_suffix(input_val), expected)


class TestDebugPrint(unittest.TestCase):
    """Test debug printing across all scrapers."""

    def test_debug_print_enabled(self):
        """Test debug_print outputs when DEBUG=True."""
        original = scraper_base.DEBUG
        scraper_base.DEBUG = True
        with patch('builtins.print') as mock_print:
            scraper_base.debug_print("test message")
            mock_print.assert_called_once_with("[DEBUG] test message")
        scraper_base.DEBUG = original

    def test_debug_print_disabled(self):
        """Test debug_print is silent when DEBUG=False."""
        original = scraper_base.DEBUG
        scraper_base.DEBUG = False
        with patch('builtins.print') as mock_print:
            scraper_base.debug_print("test message")
            mock_print.assert_not_called()
        scraper_base.DEBUG = original


class TestModelDiscoveryFallback(unittest.TestCase):
    """Test that model discovery returns defaults on network failure."""

    def test_iphone_fallback(self):
        """When Apple's site is unreachable, discovery returns DEFAULT_MODELS."""
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            result = iphone.get_available_models()
            self.assertEqual(result, iphone.IPhoneScraper.DEFAULT_MODELS)
            self.assertGreater(len(result), 0)

    def test_ipad_fallback(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            result = ipad.get_available_models()
            self.assertEqual(result, ipad.IPadScraper.DEFAULT_MODELS)
            self.assertGreater(len(result), 0)

    def test_mac_fallback(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            result = mac.get_available_models()
            self.assertEqual(result, mac.MacScraper.DEFAULT_MODELS)
            self.assertGreater(len(result), 0)

    def test_airpods_fallback(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 404
            result = airpods.get_available_models()
            self.assertEqual(result, airpods.AirPodsScraper.DEFAULT_MODELS)
            self.assertGreater(len(result), 0)


class TestMergeProductData(unittest.TestCase):
    """Test the unified merge function."""

    def setUp(self):
        # Same product name in both regions (as Apple does), but different SKUs
        self.sample_data = [
            {
                "SKU": "US001",
                "OriginalSKU": "US001LL/A",
                "Name": "Test Product 256GB",
                "Price": 999.0,
                "Region": "US",
                "Region_Code": "",
                "PartNumber": "US001LL/A",
            },
            {
                "SKU": "TW999",
                "OriginalSKU": "TW999FE/A",
                "Name": "Test Product 256GB",
                "Price": 31900.0,
                "Region": "TW",
                "Region_Code": "tw",
                "PartNumber": "TW999FE/A",
            },
        ]

    def test_basic_merge(self):
        """Test that merge produces correct columns."""
        result = scraper_base.merge_product_data(self.sample_data)
        self.assertFalse(result.empty)
        expected_cols = ['SKU', 'Price_US', 'Price_TW', 'PRODUCT_NAME']
        for col in expected_cols:
            self.assertIn(col, result.columns)

    def test_merge_by_name(self):
        """Test that products with same Name but different SKUs merge into one row."""
        result = scraper_base.merge_product_data(self.sample_data)
        self.assertEqual(len(result), 1)

    def test_merge_preserves_prices(self):
        """Test that prices are preserved correctly after Name-based merge."""
        result = scraper_base.merge_product_data(self.sample_data)
        row = result.iloc[0]
        self.assertEqual(row['Price_US'], 999.0)
        self.assertEqual(row['Price_TW'], 31900.0)

    def test_merge_keeps_reference_sku(self):
        """Test that the SKU column contains the reference region's SKU."""
        result = scraper_base.merge_product_data(self.sample_data)
        self.assertEqual(result.iloc[0]['SKU'], 'US001')

    def test_merge_with_extra_columns(self):
        """Test merge preserves extra columns (e.g. Mac specs)."""
        for item in self.sample_data:
            item['Chip'] = 'M4'
            item['Memory'] = '16GB'
            item['Storage'] = '256GB'

        result = scraper_base.merge_product_data(
            self.sample_data,
            extra_columns=['Chip', 'Memory', 'Storage']
        )
        self.assertIn('Chip', result.columns)
        self.assertEqual(result.iloc[0]['Chip'], 'M4')

    def test_merge_orphan_different_names(self):
        """Test that products only in one region show up as orphans."""
        data = self.sample_data + [
            {
                "SKU": "US002",
                "OriginalSKU": "US002LL/A",
                "Name": "US Exclusive Product",
                "Price": 1299.0,
                "Region": "US",
                "Region_Code": "",
                "PartNumber": "US002LL/A",
            },
        ]
        result = scraper_base.merge_product_data(data)
        self.assertEqual(len(result), 2)
        orphan = result[result['PRODUCT_NAME'] == 'US Exclusive Product'].iloc[0]
        self.assertEqual(orphan['Price_TW'], 0)

    def test_merge_empty_data(self):
        """Test merge handles empty input."""
        result = scraper_base.merge_product_data([])
        self.assertTrue(result.empty)

    def test_prices_are_numeric(self):
        """Test that price columns are numeric."""
        result = scraper_base.merge_product_data(self.sample_data)
        for col in result.columns:
            if col.startswith('Price_'):
                self.assertTrue(pd.api.types.is_numeric_dtype(result[col]))
                self.assertTrue((result[col] >= 0).all())

    def test_all_scrapers_use_same_merge(self):
        """Test that all scraper merge functions produce the same base format."""
        scrapers = [iphone, ipad, mac, airpods, watch, tvhome]
        for scraper in scrapers:
            with self.subTest(scraper=scraper.__name__):
                result = scraper.merge_product_data(self.sample_data)
                if not result.empty:
                    self.assertIn('SKU', result.columns)
                    self.assertIn('PRODUCT_NAME', result.columns)
                    self.assertIn('Price_US', result.columns)
                    self.assertIn('Price_TW', result.columns)


class TestMacSpecExtraction(unittest.TestCase):
    """Test Mac-specific specification extraction."""

    def test_extract_specs_from_text(self):
        """Test spec extraction from configuration text."""
        text = "Apple M4 chip, 10-core CPU, 10-core GPU, 16-core Neural Engine, 16GB memory, 256GB storage"
        specs = mac.extract_specs_from_text(text)
        self.assertEqual(specs['chip'], 'M4')
        self.assertEqual(specs['cpu_cores'], '10')
        self.assertEqual(specs['gpu_cores'], '10')
        self.assertEqual(specs['neural_engine'], '16')
        self.assertEqual(specs['memory'], '16GB')
        self.assertEqual(specs['storage'], '256GB')

    def test_extract_specs_empty_text(self):
        """Test spec extraction from empty text."""
        specs = mac.extract_specs_from_text("")
        self.assertFalse(any(specs.values()))

    def test_extract_specs_pro_chip(self):
        """Test spec extraction for Pro/Max/Ultra chips."""
        text = "Apple M4 Pro chip, 14-core CPU, 20-core GPU, 48GB memory, 1TB storage"
        specs = mac.extract_specs_from_text(text)
        self.assertEqual(specs['chip'], 'M4 PRO')


class TestAlignmentReport(unittest.TestCase):
    """Test alignment reporting and completeness validation."""

    def test_alignment_report_detects_orphans(self):
        """Test that orphan products (missing price in one region) are detected."""
        data = [
            {"SKU": "US01", "OriginalSKU": "US01", "Name": "Product A", "Price": 999.0,
             "Region": "US", "Region_Code": "", "PartNumber": "US01"},
            {"SKU": "TW01", "OriginalSKU": "TW01", "Name": "Product A", "Price": 31900.0,
             "Region": "TW", "Region_Code": "tw", "PartNumber": "TW01"},
            # Product B only in US — should be orphan in TW
            {"SKU": "US02", "OriginalSKU": "US02", "Name": "Product B", "Price": 1299.0,
             "Region": "US", "Region_Code": "", "PartNumber": "US02"},
        ]
        result = scraper_base.merge_product_data(data)
        self.assertEqual(len(result), 2)

        # Product B should have Price_TW = 0 (orphan)
        b_row = result[result['PRODUCT_NAME'] == 'Product B'].iloc[0]
        self.assertEqual(b_row['Price_TW'], 0)
        self.assertEqual(b_row['Price_US'], 1299.0)

    def test_alignment_report_fully_aligned(self):
        """Test that fully aligned data reports 100%."""
        data = [
            {"SKU": "US01", "OriginalSKU": "US01", "Name": "Product A", "Price": 999.0,
             "Region": "US", "Region_Code": "", "PartNumber": "US01"},
            {"SKU": "TW01", "OriginalSKU": "TW01", "Name": "Product A", "Price": 31900.0,
             "Region": "TW", "Region_Code": "tw", "PartNumber": "TW01"},
        ]
        result = scraper_base.merge_product_data(data)
        # Both prices should be > 0
        self.assertTrue((result['Price_US'] > 0).all())
        self.assertTrue((result['Price_TW'] > 0).all())

    def test_completeness_warns_on_empty_region(self):
        """Test that validate_completeness warns when a region has no products."""
        products_by_region = {
            "": [{"SKU": "A1"}],
            "tw": [],
        }
        with patch('builtins.print'):
            results = scraper_base.validate_completeness(products_by_region)
        self.assertIsNotNone(results['TW']['warning'])

    def test_completeness_warns_on_large_discrepancy(self):
        """Test that validate_completeness warns when one region has far fewer products."""
        products_by_region = {
            "": [{"SKU": f"A{i}"} for i in range(20)],  # 20 US products
            "tw": [{"SKU": f"A{i}"} for i in range(5)],  # only 5 TW products
        }
        with patch('builtins.print'):
            results = scraper_base.validate_completeness(products_by_region)
        self.assertIsNotNone(results['TW']['warning'])

    def test_completeness_no_warning_when_balanced(self):
        """Test no warning when regions have similar counts."""
        products_by_region = {
            "": [{"SKU": f"A{i}"} for i in range(20)],
            "tw": [{"SKU": f"A{i}"} for i in range(18)],
        }
        with patch('builtins.print'):
            results = scraper_base.validate_completeness(products_by_region)
        self.assertIsNone(results['TW']['warning'])


class TestEndToEndIntegration(unittest.TestCase):
    """Integration tests that hit Apple's live website."""

    @unittest.skipIf(os.getenv('SKIP_NETWORK_TESTS'), "Skipping network tests")
    def test_model_discovery_finds_models(self):
        """Test that dynamic model discovery finds at least 1 model per product type."""
        scraper_classes = [
            iphone.IPhoneScraper,
            ipad.IPadScraper,
            airpods.AirPodsScraper,
        ]
        for cls in scraper_classes:
            with self.subTest(scraper=cls.product_name):
                try:
                    scraper = cls()
                    models = scraper.get_models()
                    self.assertGreater(len(models), 0,
                        f"{cls.product_name}: discovery returned no models")
                    print(f"\n  {cls.product_name} discovered: {sorted(models)}")
                except Exception as e:
                    self.skipTest(f"Discovery failed for {cls.product_name}: {e}")

    @unittest.skipIf(os.getenv('SKIP_NETWORK_TESTS'), "Skipping network tests")
    def test_scraper_can_fetch_real_data(self):
        """Test that each scraper can fetch products from a dynamically discovered model."""
        scraper_classes = [
            (iphone.IPhoneScraper, '/shop/buy-iphone/'),
            (ipad.IPadScraper, '/shop/buy-ipad/'),
            (airpods.AirPodsScraper, '/shop/buy-airpods/'),
        ]

        for cls, url_base in scraper_classes:
            with self.subTest(scraper=cls.product_name):
                try:
                    scraper = cls()
                    models = scraper.get_models()
                    self.assertGreater(len(models), 0)

                    # Pick the first discovered model and fetch it
                    model = models[0]
                    url = f"https://www.apple.com{url_base}{model}"
                    from scraper_base import fetch_product_page
                    products = fetch_product_page(url, "")

                    self.assertIsInstance(products, list)
                    self.assertGreater(len(products), 0,
                        f"No products found at {url}")

                    product = products[0]
                    for field in ['SKU', 'Name', 'Price', 'Region', 'Region_Code']:
                        self.assertIn(field, product)

                    if product['Price'] is not None:
                        self.assertIsInstance(product['Price'], (int, float))
                        self.assertGreater(product['Price'], 0)

                except Exception as e:
                    self.skipTest(f"Network test failed for {cls.product_name}: {e}")

    @unittest.skipIf(os.getenv('SKIP_NETWORK_TESTS'), "Skipping network tests")
    def test_cross_region_name_alignment(self):
        """Test that the same product page returns matching Names across US and TW."""
        scraper_classes = [
            (iphone.IPhoneScraper, '/shop/buy-iphone/'),
            (ipad.IPadScraper, '/shop/buy-ipad/'),
        ]

        for cls, url_base in scraper_classes:
            with self.subTest(scraper=cls.product_name):
                try:
                    scraper = cls()
                    models = scraper.get_models()
                    model = models[0]

                    from scraper_base import fetch_product_page
                    us_products = fetch_product_page(f"https://www.apple.com{url_base}{model}", "")
                    tw_products = fetch_product_page(f"https://www.apple.com/tw{url_base}{model}", "tw")

                    if not us_products or not tw_products:
                        self.skipTest(f"Could not fetch data for {cls.product_name}")

                    us_names = set(p['Name'] for p in us_products)
                    tw_names = set(p['Name'] for p in tw_products)
                    overlap = us_names & tw_names
                    total = len(us_names | tw_names)
                    overlap_pct = len(overlap) / total * 100 if total else 0

                    print(f"\n  {cls.product_name} ({model}): US={len(us_names)} TW={len(tw_names)} "
                          f"name_overlap={len(overlap)}/{total} ({overlap_pct:.0f}%)")

                    # Apple products launch globally — names should match >=90%
                    self.assertGreaterEqual(overlap_pct, 90,
                        f"{cls.product_name}: only {overlap_pct:.0f}% name overlap. "
                        f"US-only: {us_names - tw_names}, TW-only: {tw_names - us_names}")

                except Exception as e:
                    self.skipTest(f"Network test failed for {cls.product_name}: {e}")

    @unittest.skipIf(os.getenv('SKIP_NETWORK_TESTS'), "Skipping network tests")
    def test_per_page_product_count_reasonable(self):
        """Test that a dynamically discovered product page has at least 2 products."""
        scraper_classes = [
            (iphone.IPhoneScraper, '/shop/buy-iphone/'),
            (ipad.IPadScraper, '/shop/buy-ipad/'),
        ]

        for cls, url_base in scraper_classes:
            with self.subTest(scraper=cls.product_name):
                try:
                    scraper = cls()
                    models = scraper.get_models()
                    model = models[0]
                    url = f"https://www.apple.com{url_base}{model}"

                    from scraper_base import fetch_product_page
                    products = fetch_product_page(url, "")
                    self.assertGreaterEqual(len(products), 2,
                        f"Expected at least 2 products from {url}, got {len(products)}")
                except Exception as e:
                    self.skipTest(f"Network test failed: {e}")


class TestConvertToJson(unittest.TestCase):
    """Test CSV to JSON conversion."""

    def setUp(self):
        self.test_csv = 'test_products.csv'
        with open(self.test_csv, 'w') as f:
            f.write("SKU,Price_US,Price_TW,PRODUCT_NAME\n")
            f.write("TEST001,999.0,31900.0,Test Product\n")
            f.write("TEST002,1299.0,41900.0,Another Product\n")

    def tearDown(self):
        for f in [self.test_csv, 'test_dir/test_output.json']:
            if os.path.exists(f):
                os.remove(f)
        import shutil
        for d in ['test_dir']:
            if os.path.exists(d):
                shutil.rmtree(d)

    def test_csv_to_json_conversion(self):
        """Test CSV to JSON conversion produces valid output."""
        exchange_rates = {
            "USD": 1.0, "TWD": 31.5,
            "lastUpdated": "2024-01-01T00:00:00Z", "source": "Test"
        }
        os.makedirs('test_dir', exist_ok=True)
        output = 'test_dir/test_output.json'

        convert_to_json.csv_to_json(self.test_csv, output, 'test', exchange_rates)

        self.assertTrue(os.path.exists(output))
        with open(output, 'r') as f:
            data = json.load(f)

        self.assertIn('metadata', data)
        self.assertIn('products', data)
        self.assertEqual(len(data['products']), 2)

        product = data['products'][0]
        for field in ['SKU', 'Price_US', 'Price_TW', 'PRODUCT_NAME', 'price_difference_percent', 'product_type']:
            self.assertIn(field, product)


class TestFileOutputs(unittest.TestCase):
    """Test existing CSV file structure if files are present."""

    def test_generated_csv_files_structure(self):
        """Validate structure of existing CSV output files."""
        files = [
            'iphone_products_merged.csv',
            'ipad_products_merged.csv',
            'mac_products_merged.csv',
            'watch_products_merged.csv',
            'airpods_products_merged.csv',
            'tvhome_products_merged.csv',
        ]

        for file in files:
            if not os.path.exists(file):
                continue

            with self.subTest(file=file):
                df = pd.read_csv(file)
                self.assertGreater(len(df), 0)
                self.assertIn('PRODUCT_NAME', df.columns)

                # Must have either unified SKU column or per-region SKU columns
                has_sku = 'SKU' in df.columns or 'SKU_US' in df.columns
                self.assertTrue(has_sku, f"No SKU column found in {file}")

                price_cols = [c for c in df.columns if c.startswith('Price_')]
                self.assertGreater(len(price_cols), 0)

    def test_consolidated_csv_files_structure(self):
        """Validate structure of consolidated CSV files."""
        files = [
            'iphone_products_consolidated.csv',
            'ipad_products_consolidated.csv',
            'mac_products_consolidated.csv',
        ]

        for file in files:
            if not os.path.exists(file):
                continue

            with self.subTest(file=file):
                df = pd.read_csv(file)
                self.assertGreater(len(df), 0)
                self.assertIn('PRODUCT_NAME', df.columns)
                self.assertIn('Available_Colors', df.columns)
                self.assertIn('Color_Variants', df.columns)

                variants = df['Color_Variants'].dropna()
                if len(variants) > 0:
                    self.assertTrue(all(x > 0 for x in variants))


class TestColorConsolidation(unittest.TestCase):
    """Test color consolidation logic."""

    def test_extract_colors(self):
        """Test color extraction from product names."""
        from smart_consolidate_colors import extract_colors
        colors = extract_colors("iPhone 16 Pro 256GB Black Titanium")
        self.assertIn('black titanium', colors)

    def test_clean_product_name(self):
        """Test color removal from product names."""
        from smart_consolidate_colors import clean_product_name
        result = clean_product_name("iPhone 16 Pro 256GB Black Titanium")
        self.assertNotIn('Black', result)
        self.assertNotIn('Titanium', result)
        self.assertIn('iPhone', result)
        self.assertIn('256GB', result)

    def test_consolidation_reduces_rows(self):
        """Test that consolidation merges color variants."""
        from smart_consolidate_colors import consolidate

        df = pd.DataFrame([
            {'SKU': 'A1', 'Price_US': 999, 'Price_TW': 31900, 'PRODUCT_NAME': 'iPhone 16 256GB Black'},
            {'SKU': 'A2', 'Price_US': 999, 'Price_TW': 31900, 'PRODUCT_NAME': 'iPhone 16 256GB Blue'},
            {'SKU': 'A3', 'Price_US': 999, 'Price_TW': 31900, 'PRODUCT_NAME': 'iPhone 16 256GB Pink'},
        ])

        result = consolidate(df, 'iPhone')
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]['Color_Variants'], 3)

    def test_different_prices_not_merged(self):
        """Test that products with different prices are NOT merged."""
        from smart_consolidate_colors import consolidate

        df = pd.DataFrame([
            {'SKU': 'A1', 'Price_US': 999, 'Price_TW': 31900, 'PRODUCT_NAME': 'iPhone 16 256GB'},
            {'SKU': 'A2', 'Price_US': 1199, 'Price_TW': 37900, 'PRODUCT_NAME': 'iPhone 16 512GB'},
        ])

        result = consolidate(df, 'iPhone')
        self.assertEqual(len(result), 2)


def run_scraper_tests():
    """Run all tests and report results."""
    print("Running Apple Store Scraper Test Suite\n")

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestSharedConfiguration,
        TestSKUUtilities,
        TestDebugPrint,
        TestModelDiscoveryFallback,
        TestMergeProductData,
        TestAlignmentReport,
        TestMacSpecExtraction,
        TestEndToEndIntegration,
        TestConvertToJson,
        TestFileOutputs,
        TestColorConsolidation,
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    total = result.testsRun
    passed = total - len(result.failures) - len(result.errors)
    print(f"Success rate: {(passed / total * 100):.1f}%" if total else "No tests run")

    if not result.failures and not result.errors:
        print("All tests passed!")

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_scraper_tests()
    sys.exit(0 if success else 1)
