# Apple Store Scraper

Apple Store Scraper is a tool for scraping iPhone and iPad product pricing information from the Apple online store. This tool allows for comparison of Apple product prices between the United States and Taiwan regions, helping consumers understand price differences across different markets.

## Features

- Scrapes the latest iPhone and iPad product information
- Compares prices between US and Taiwan regions simultaneously
- Provides complete product names (in English)
- Automatically organizes data into CSV format
- Matches and merges data by SKU for each product model

## Requirements

- Python 3.6+
- Required Python packages:
  - requests
  - beautifulsoup4
  - pandas

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/apple-store-scrape.git
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
1. Scrape iPhone product information from both US and Taiwan Apple official stores
2. Process and merge the data
3. Save the results to an `iphone_products_merged.csv` file

### Scraping iPad Product Information

Run the following command to scrape iPad product information:

```bash
python ipad.py
```

This command will:
1. Scrape iPad product information from both US and Taiwan Apple official stores
2. Process and merge the data
3. Save the results to an `ipad_products_merged.csv` file

## Output Data Format

The generated CSV files contain the following fields:

| Field | Description |
|------|------|
| SKU | Unique product identifier |
| 台灣價格 (Taiwan Price) | Price in Taiwan (TWD) |
| 美國價格 (US Price) | Price in the US (USD) |
| 台灣產品名 (Taiwan Product Name) | Product name as sold in Taiwan |
| 美國產品名 (US Product Name) | Product name as sold in the US |

## Development

### Project Structure

```
apple-store-scrape/
│
├── .venv/                  # Python virtual environment
├── iphone.py               # iPhone data scraping script
├── iphone_products_merged.csv  # iPhone product data output
├── ipad.py                 # iPad data scraping script
├── ipad_products_merged.csv    # iPad product data output
└── requirements.txt        # Project dependencies
```

### Data Processing Flow

1. **Data Scraping**:
   - Use `requests` to access Apple's official product pages
   - Parse HTML content using `BeautifulSoup`
   - Extract JSON data containing product information

2. **Data Processing**:
   - Extract product details from JSON (SKU, price, name, etc.)
   - Separate product data for US and Taiwan
   - Process and manipulate data using `pandas`

3. **Data Merging**:
   - Merge product data from US and Taiwan based on SKU
   - Handle missing values and duplicate data
   - Rename columns to provide intuitive labels

4. **Data Export**:
   - Save processed data in CSV format
   - Use `utf-8-sig` encoding to ensure proper display of characters

### Extending and Customizing

This project can be extended in the following ways:

1. **Add More Product Categories**:
   - Copy existing scripts and modify URLs and product models
   - Adjust data processing logic to accommodate new product categories

2. **Add More Regions**:
   - Add more country/region URLs to the loop
   - Extend data processing logic to support multi-country comparison

3. **Add More Analysis Features**:
   - Calculate price differences and currency conversions
   - Generate price trend charts
   - Set up price change alerts

## Technical Details

### Data Sources

Data is sourced from Apple's official product pages:
- US: https://www.apple.com/shop/buy-iphone/
- Taiwan: https://www.apple.com/tw/shop/buy-iphone/

The script specifically looks for a `<script>` tag with `id="metrics"` in the page, which contains complete product information, including SKU, price, and configuration details.

### Error Handling

The script includes basic error handling mechanisms:
- Checking HTTP response status codes
- Validating JSON data structures
- Handling null values and missing data

### Notes

- Apple may change its website structure; if the script stops working, the HTML parsing logic may need to be updated
- This script is for personal research and comparison only, please respect Apple's terms of service
- Please do not run this script too frequently to avoid unnecessary load on Apple's servers
- Rate limiting has been implemented (1 second delay between requests) to be respectful to Apple's servers

## Ethical Considerations

This tool is designed for educational and personal use only. When using this scraper, please:

1. Be respectful of Apple's servers by not making excessive requests
2. Do not use this tool for commercial purposes without proper authorization
3. Respect Apple's terms of service
4. Be aware that website scraping may be against the terms of service of some websites

## Disclaimer

This project is not affiliated with, authorized by, or endorsed by Apple Inc. All product names, logos, and brands are the property of their respective owners.
