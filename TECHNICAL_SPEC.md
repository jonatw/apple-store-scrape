# Apple Store Scraper - Technical Specification

## Overview

Apple Store Scraper is a Python tool for scraping product information from the Apple online store. The tool focuses on automating the collection of iPhone and iPad product prices and details, and performing cross-region comparisons (currently supporting the US and Taiwan regions).

## System Requirements

- **Operating System**: Cross-platform (Windows, macOS, Linux)
- **Python Version**: Python 3.6 or higher
- **Memory Requirements**: Minimum 512MB RAM
- **Storage Space**: Minimum 10MB available space

## Dependencies

| Package Name | Version | Purpose |
|---------|------|------|
| requests | 2.32.3 | Handling HTTP requests |
| beautifulsoup4 | 4.12.3 | HTML parsing |
| pandas | 2.2.3 | Data processing and analysis |

## Module Descriptions

### iphone.py

iPhone product information scraping module, with the following main functions:

#### Main Functions

- `extract_product_details(url, is_taiwan=False)`:
  - **Input**:
    - `url` (string): URL of the Apple store product page
    - `is_taiwan` (boolean): Flag indicating whether the region is Taiwan
  - **Process**:
    1. Send HTTP GET request to the specified URL
    2. Parse HTML and locate product information JSON
    3. Extract product details
  - **Output**:
    - List of dictionaries containing product details

#### Data Processing Steps

1. Iterate through all iPhone models (iphone-16-pro, iphone-16, iphone-15, iphone-14, iphone-se)
2. Process both US and Taiwan URLs
3. Merge data and differentiate Taiwan/US product information
4. Handle null values and duplicates
5. Output to CSV format

### ipad.py

iPad product information scraping module, with the following main functions:

#### Main Functions

- `extract_product_details(url, is_taiwan=False)`:
  - **Input**:
    - `url` (string): URL of the Apple store product page
    - `is_taiwan` (boolean): Flag indicating whether the region is Taiwan
  - **Process**:
    1. Send HTTP GET request to the specified URL
    2. Parse HTML and locate product information JSON
    3. Extract product details
  - **Output**:
    - List of dictionaries containing product details

#### Data Processing Steps

1. Iterate through all iPad models (ipad-pro, ipad-air, ipad, ipad-mini)
2. Process both US and Taiwan URLs
3. Merge data and differentiate Taiwan/US product information
4. Handle null values and duplicates
5. Output to CSV format

## Data Structures

### Input Data

Example of JSON structure scraped from the webpage (simplified):
```json
{
  "data": {
    "products": [
      {
        "sku": "MYMG3",
        "name": "iPhone 16 Pro 256GB Black Titanium",
        "price": {
          "fullPrice": 1099.0
        },
        "category": "iphone",
        "partNumber": "MYMG3LL/A"
      }
    ]
  }
}
```

### Output Data

CSV files contain the following fields:
- **SKU**: Unique product identifier
- **台灣價格 (Taiwan Price)**: Price in Taiwan (TWD)
- **美國價格 (US Price)**: Price in the US (USD)
- **台灣產品名 (Taiwan Product Name)**: Product name as sold in Taiwan
- **美國產品名 (US Product Name)**: Product name as sold in the US

## API and Data Sources

### Source Endpoints

- US iPhone: `https://www.apple.com/shop/buy-iphone/[model]`
- Taiwan iPhone: `https://www.apple.com/tw/shop/buy-iphone/[model]`
- US iPad: `https://www.apple.com/shop/buy-ipad/[model]`
- Taiwan iPad: `https://www.apple.com/tw/shop/buy-ipad/[model]`

### Data Extraction Location

In the HTML, product information is contained in the following tag:
```
<script type="application/json" id="metrics">...</script>
```

## Execution Flow

1. **Initialization**:
   - Set URL base template
   - Define product model list
   
2. **Data Scraping**:
   - Loop through each product model
   - Create US and Taiwan URLs for each model
   - Scrape and parse each page
   
3. **Data Processing**:
   - Extract product details
   - Mark data according to region
   - Populate appropriate fields (price, product name)
   
4. **Data Merging**:
   - Merge data from different regions using SKU as key
   - Handle missing values and duplicates
   
5. **Output Results**:
   - Rename columns
   - Save as CSV file

## Performance Considerations

- **Execution Time**: Depending on network conditions, a complete scrape may take 5-30 seconds
- **Resource Usage**:
  - Memory Usage: Peak approximately 50-100MB
  - CPU Usage: Low to moderate
  - Network Usage: Approximately 5-10MB data transfer per execution

## Limitations and Constraints

- Dependent on Apple's HTML structure; if Apple changes its website design, the script may need to be updated
- Does not include real-time currency conversion
- No persistent storage mechanism; each execution overwrites previous output files
- No automated scheduling functionality; requires manual execution

## Extensibility

The system is designed to be modular and can be extended in the following ways:

- Add more product categories (like Mac, Watch, etc.)
- Expand to more regions/countries
- Implement historical data tracking
- Add price difference analysis functionality
- Integrate currency conversion

## Error Handling

Includes basic error handling mechanisms:
- Checking HTTP response status (200 OK)
- Validating JSON data structure conformance
- Handling missing data and null values
- Providing diagnostic information when errors occur

## Version Changelog

### Version 1.0.0
- Initial version
- Support for iPhone and iPad product information scraping
- Support for US and Taiwan region comparison