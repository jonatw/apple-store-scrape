# Apple Store Scraper

Apple Store Scraper is a tool for scraping iPhone and iPad product pricing information from the Apple online store. This tool allows for comparison of Apple product prices across multiple regions (currently configured for the United States and Taiwan), helping consumers understand price differences across different markets.

## Features

- Scrapes the latest iPhone and iPad product information from Apple's online store
- Dynamically detects available iPhone and iPad models from Apple's website
- Supports multi-region comparison (configurable through REGIONS dictionary)
- Dynamically extracts colors from product names rather than using hardcoded lists
- Uses standardized product names for accurate product matching across regions
- Automatically organizes data into CSV format with region-specific columns
- Intelligent product matching system that works across different regions

## Requirements

- Python 3.6+
- Required Python packages:
  - requests==2.32.3
  - beautifulsoup4==4.12.3
  - pandas==2.2.3

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jonatw/apple-store-scrape.git
cd apple-store-scrape
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

## Usage

### Scraping iPhone Product Information

Run the following command to scrape iPhone product information:

```bash
python iphone.py
```

This command will:
1. Dynamically identify available iPhone models from Apple's website
2. Scrape iPhone product information from all configured regions (US and Taiwan by default)
3. Process and merge the data using standardized product names for matching
4. Save the results to an `iphone_products_merged.csv` file with columns for SKUs, prices, and product names

### Scraping iPad Product Information

Run the following command to scrape iPad product information:

```bash
python ipad.py
```

This command will:
1. Dynamically identify available iPad models from Apple's website
2. Scrape iPad product information from all configured regions (US and Taiwan by default)
3. Process and merge the data using SKU for matching
4. Save the results to an `ipad_products_merged.csv` file with columns for SKU, region-specific prices, and product name

## Configuration

Both scripts have a configuration section at the top where you can:

- Modify the `REGIONS` dictionary to add or remove regions
- Change the `REFERENCE_REGION` for product naming
- Adjust the `REQUEST_DELAY` to control the rate of requests
- Toggle `DEBUG` mode for verbose output

Example to add Japan as a region:
```python
REGIONS = {
    "": ["US", "USD", "en-us", "$"],       # United States
    "tw": ["TW", "TWD", "zh-tw", "NT$"],   # Taiwan
    "jp": ["JP", "JPY", "ja-jp", "¥"],      # Japan
}
```

## Output Data Format

### iPhone Output Format
The iPhone CSV file contains the following structure:
- Region-specific SKU columns (e.g., `SKU_US`, `SKU_TW`)
- Region-specific price columns (e.g., `Price_US`, `Price_TW`)
- `PRODUCT_NAME` - The product name from the reference region

### iPad Output Format
The iPad CSV file contains the following structure:
- `SKU` - Common identifier across regions
- Region-specific price columns (e.g., `Price_US`, `Price_TW`)
- `PRODUCT_NAME` - The product name from the reference region

## Development

### Project Structure

```
apple-store-scrape/
│
├── .venv/                     # Python virtual environment
├── iphone.py                  # iPhone data scraping script with multi-region support
├── iphone_products_merged.csv # iPhone product data output
├── ipad.py                    # iPad data scraping script with multi-region support
├── ipad_products_merged.csv   # iPad product data output
├── README.md                  # Project documentation
├── TECHNICAL_SPEC.md          # Technical specifications document
└── requirements.txt           # Project dependencies
```

### Data Processing Flow

1. **Model Detection**:
   - Dynamically identify available models from Apple's website
   - Fallback to default model list if website structure changes

2. **Data Scraping**:
   - Iterate through detected models for each configured region
   - Use `requests` to access Apple's official product pages
   - Parse HTML content using `BeautifulSoup`
   - Extract JSON data containing product information

3. **Data Processing**:
   - For iPhone: Use standardized product names for matching across regions
   - For iPad: Use SKU for matching products
   - Process data for each region separately
   - Handle color and model variations across regions

4. **Data Merging**:
   - Merge products from different regions based on matching strategy
   - Create region-specific columns for SKUs and prices
   - Handle missing values and duplicate data
   - Organize columns in a consistent format

5. **Data Export**:
   - Save processed data in CSV format
   - Use `utf-8-sig` encoding to ensure proper display of characters

### Extending the Project

You can extend this project in the following ways:

1. **Add More Regions**:
   - Add new entries to the `REGIONS` dictionary in the scripts
   - The format is: `"region_code": ["Display_Name", "Currency_Code", "Locale", "Currency_Symbol"]`
   - Example: `"uk": ["UK", "GBP", "en-gb", "£"]`

2. **Add More Product Categories**:
   - Create new scripts following the pattern of `iphone.py` or `ipad.py`
   - Update the URL patterns and adjust the product detection logic as needed

3. **Add Analysis Features**:
   - Implement currency conversion between regions
   - Calculate price differences and price indexes
   - Generate visualizations and trends

## Technical Details

### Data Sources

Data is sourced from Apple's official product pages:
- Apple Store Base URLs: 
  - US: `https://www.apple.com/shop/buy-{product}/`
  - Taiwan: `https://www.apple.com/tw/shop/buy-{product}/`
  - Other regions follow the same pattern

The scripts specifically look for a `<script>` tag with `id="metrics"` in the page, which contains complete product information, including SKU, price, and configuration details.

### Error Handling

The scripts include several error handling mechanisms:
- Dynamic model detection with fallback to default lists
- HTTP response status code validation
- JSON data structure validation
- Debugging output when `DEBUG = True`
- Fill strategies for missing data

## Notes and Limitations

- Apple may change its website structure; if scripts stop working, the HTML parsing logic may need to be updated
- This tool is for personal research and comparison only, please respect Apple's terms of service
- The scripts implement rate limiting (1 second delay between requests) to be respectful to Apple's servers
- Currency conversion is not implemented; prices are shown in their original currencies

## Ethical Considerations

This tool is designed for educational and personal use only. When using this scraper, please:

1. Be respectful of Apple's servers by not making excessive requests
2. Do not use this tool for commercial purposes without proper authorization
3. Respect Apple's terms of service
4. Be aware that website scraping may be against the terms of service of some websites

## Disclaimer

This project is not affiliated with, authorized by, or endorsed by Apple Inc. All product names, logos, and brands are the property of their respective owners.