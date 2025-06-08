# Test Guide for Apple Store Scraper

## Overview
This document describes the comprehensive testing framework for the Apple Store Scraper project. The test suite ensures data integrity, functionality, and reliability across all scrapers.

## Test Files

### 1. `test_scrapers.py`
Main test suite covering all scraper functionality.

**Test Categories:**
- **Data Integrity Tests**: Product name standardization, configuration consistency
- **Function Tests**: Debug functions, model detection fallbacks
- **Data Validation**: Merge operations, price data types
- **Integration Tests**: End-to-end scraping from Apple's website
- **JSON Conversion**: CSV to JSON transformation
- **File Output**: CSV generation validation

### 2. `test_data_validator.py`
Specialized data validation for scraped output.

**Validation Categories:**
- **CSV Structure**: Column validation, data completeness
- **Price Data**: Numeric validation, reasonable price ranges
- **Product Names**: Consistency checks, naming conventions
- **JSON Format**: Structure validation, metadata checks
- **Exchange Rates**: Currency data validation, freshness checks

## Running Tests

### Quick Tests (No Network)
```bash
npm run test-quick
```
- Runs all tests except network integration
- Uses mocked data and fallback mechanisms
- Fast execution (~0.02 seconds)

### Full Test Suite
```bash
npm run test
```
- Includes network integration tests
- Tests actual Apple website connectivity
- Longer execution time (~6+ seconds)

### Network Only Tests
```bash
npm run test-network
```
- Only runs end-to-end integration tests
- Validates real data fetching capability
- Useful for debugging network issues

### Data Validation
```bash
python test_data_validator.py
```
- Validates existing scraped data files
- Checks data integrity and format compliance
- Reports validation summary with errors/warnings

## Test Results Analysis

### Success Metrics
- **100% pass rate** for core functionality tests
- **Valid data structure** for all product types
- **Network connectivity** to Apple's servers
- **Data consistency** across regions

### Common Issues and Solutions

#### Network Test Failures
- **Cause**: Apple website structure changes or network issues
- **Solution**: Check Apple's website manually, update selectors if needed

#### Data Validation Warnings
- **Price Range Warnings**: Products outside expected price ranges
- **Missing Data**: Zero prices or empty fields
- **Exchange Rate Age**: Rates older than 7 days

#### CSV Structure Errors
- **Missing Columns**: Required columns not present in output
- **Empty Files**: No data scraped successfully
- **Encoding Issues**: UTF-8 BOM handling problems

## Test Coverage

### iPhone Scraper Tests
- ✅ Product name standardization (regex patterns)
- ✅ Region-specific URL handling
- ✅ Price data extraction and validation
- ✅ SKU matching across regions
- ✅ CSV output format verification

### iPad Scraper Tests
- ✅ Model detection and fallback
- ✅ SKU-based product matching
- ✅ Price data consistency
- ✅ Regional configuration handling
- ✅ JSON conversion compatibility

### Mac Scraper Tests
- ✅ Complex product naming (iMac, MacBook, Mac Studio, etc.)
- ✅ Display product handling (Studio Display, Pro Display XDR)
- ✅ Price range validation (higher-end products)
- ✅ Multi-category support
- ✅ Error handling for model variations

### Data Conversion Tests
- ✅ CSV to JSON transformation
- ✅ Exchange rate integration
- ✅ Metadata generation
- ✅ Price difference calculations
- ✅ Output directory creation

## Adding New Tests

### For New Scrapers
1. Add test cases to `TestScraperDataIntegrity`
2. Include configuration consistency checks
3. Add product-specific validation rules
4. Update integration tests with sample URLs

### For New Data Fields
1. Update validation schemas in `test_data_validator.py`
2. Add field presence checks
3. Include data type validation
4. Test null/empty value handling

### For New Regions
1. Update region configuration tests
2. Add currency validation
3. Test locale-specific formatting
4. Validate exchange rate handling

## Performance Benchmarks

### Test Execution Times
- **Unit Tests**: < 0.02 seconds
- **Integration Tests**: 3-8 seconds per scraper
- **Data Validation**: < 1 second
- **Full Suite**: < 10 seconds

### Memory Usage
- **Test Environment**: < 50MB RAM
- **Scraper Execution**: < 100MB RAM
- **Data Processing**: < 200MB RAM

## Continuous Integration

### GitHub Actions Integration
The test suite integrates with GitHub Actions for automated testing:

```yaml
# Example workflow step
- name: Run Tests
  run: |
    npm run test-quick
    python test_data_validator.py
```

### Pre-commit Hooks
Recommended pre-commit hook:

```bash
#!/bin/sh
npm run test-quick
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Debugging Test Failures

### Debug Mode
Enable debug output in scrapers:
```python
DEBUG = True  # in scraper configuration
```

### Verbose Test Output
```bash
python -m unittest test_scrapers -v
```

### Individual Test Execution
```bash
python -m unittest test_scrapers.TestDataValidation.test_price_data_types -v
```

### Network Debugging
```bash
# Test specific scraper connectivity
python -c "import iphone; print(iphone.get_available_models())"
```

## Test Data

### Sample Data Files
- `test_products.csv`: Minimal test dataset
- Generated during test execution and cleaned up
- Covers basic price and product structure

### Mock Data
- Exchange rates: USD=1.0, TWD=31.5
- Sample products: iPhone and test products
- Regional variations: US and Taiwan

## Best Practices

### Test Writing
1. **Isolation**: Each test should be independent
2. **Cleanup**: Always clean up test files
3. **Mocking**: Use mocks for external dependencies
4. **Assertions**: Be specific about what you're testing

### Data Validation
1. **Range Checks**: Validate reasonable price ranges
2. **Type Checking**: Ensure numeric data is numeric
3. **Completeness**: Check for missing required fields
4. **Consistency**: Validate cross-regional data consistency

### Error Handling
1. **Graceful Degradation**: Tests should handle failures gracefully
2. **Informative Messages**: Provide clear error descriptions
3. **Recovery**: Implement fallback mechanisms
4. **Logging**: Include sufficient debug information

## Maintenance

### Regular Tasks
- Update test data when Apple changes product lines
- Refresh expected price ranges quarterly
- Validate test URLs are still accessible
- Update exchange rate test thresholds

### When Apple Updates Their Website
1. Run network tests to identify failures
2. Update selectors if needed
3. Refresh default model lists
4. Validate new product categories

This comprehensive test suite ensures the reliability and accuracy of the Apple Store Scraper across all supported product categories and regions.