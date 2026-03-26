# Apple Store Scraper - Technical Specification

## Overview

Apple Store Scraper is a Python tool for scraping product information from the Apple online store across multiple regions. It collects pricing data for all major Apple product categories, consolidates color variants, and generates a responsive web comparison interface.

## System Requirements

- **Python**: 3.10+
- **Node.js**: 20.x+ (for web interface and build)
- **OS**: Cross-platform (Windows, macOS, Linux)

## Dependencies

### Python Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| requests | 2.32.3 | HTTP requests to Apple Store pages |
| beautifulsoup4 | 4.13.4 | HTML parsing for product data extraction |
| pandas | 2.2.3 | Data processing, merging, and CSV I/O |

### Frontend Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| bootstrap | 5.3.6 | Responsive UI framework |
| @popperjs/core | 2.11.8 | Positioning engine for UI components |
| vite | 6.3.5 | Build tool and development server |
| sass | 1.87.0 | SCSS compilation |
| @playwright/test | 1.52.0 | E2E testing |

## Architecture

### Shared Scraper Framework (`scraper_base.py`)

All product scrapers share a common framework to eliminate code duplication.

#### Configuration

```python
REGIONS = {
    "": ["US", "USD", "en-us", "$"],       # United States (empty = no URL prefix)
    "tw": ["TW", "TWD", "zh-tw", "NT$"],   # Taiwan
}
REFERENCE_REGION = list(REGIONS.keys())[0]  # US is the reference
REQUEST_DELAY = 1                            # seconds between requests
```

#### Dual-Strategy Product Extraction

Apple Store pages embed product data in two different formats depending on the product type:

**Strategy 1 — Metrics JSON** (iPhone, iPad, TV/Home):
```html
<script type="application/json" id="metrics">
  {"data": {"products": [{"sku": "...", "name": "...", "price": {"fullPrice": 999.0}, ...}]}}
</script>
```
- Structured, easy to parse
- Product `name` field is identical across regions (English in all locales)
- Note: Some TW pages use Unicode non-breaking space (U+00A0) instead of regular space — the framework normalizes this before matching

**Strategy 2 — Bootstrap JS** (Mac, Watch, some AirPods):
```javascript
window.PRODUCT_SELECTION_BOOTSTRAP = [{productSelectionData: {...}}]
```
- Embedded in a JS variable, extracted via brace-counting parser
- Product names differ by locale (e.g. "Mac mini" in US, "Mac mini (台灣)" in TW page title)
- Prices may be in `displayValues.prices` OR `mainDisplayValues.prices`
- Part numbers use `btrOrFdPartNumber` instead of `partNumber` on some pages
- `priceKey` field (e.g. `m4-10-10`, `13inch-midnight-10-10`) is a configuration identifier shared across regions

#### Cross-Region Merge Strategy

**Apple uses different part numbers per region for the same product.** For example, iPhone 17 Pro 256GB Silver might be `MG7K4LL/A` in US and a completely different part number in TW. SKU-based matching does NOT work.

The merge function automatically selects the best key:

| Data Source | Merge Key | Why |
|-------------|-----------|-----|
| Metrics JSON | `Name` | Product names are identical across regions |
| Bootstrap JS | `ConfigKey` (= `priceKey`) | Configuration identifiers are shared across regions; names are locale-dependent |

The function checks: if all products have a non-empty `ConfigKey`, use it; otherwise use `Name`.

#### Alignment Reporting

After every merge, the framework automatically reports:
- Total unique products and how many are fully aligned (have prices in all regions)
- Orphan products (missing price in one or more regions) with their SKU and name
- Completeness warnings if a region has far fewer products than others (possible incomplete scrape)

#### Dynamic Model Discovery

Models are discovered at runtime from Apple's landing pages:
- **Store pages** (`/shop/buy-iphone/`): `discover_models()` finds links matching the pattern
- **Marketing pages** (`/airpods/`, `/watch/`): `discover_models_from_goto()` finds `/shop/goto/` links

Each scraper filters discovery results to remove non-product links (e.g. `carrier-offers`, `studio-display`).

`DEFAULT_MODELS` are last-resort fallbacks only used when Apple's website is completely unreachable.

### Product Scrapers

Each scraper is a thin subclass of `AppleStoreScraper`:

| File | Class | Discovery | Merge Key | Special Handling |
|------|-------|-----------|-----------|-----------------|
| `iphone.py` | `IPhoneScraper` | `/shop/buy-iphone/` links | Name | Filters to `iphone*` slugs |
| `ipad.py` | `IPadScraper` | `/shop/buy-ipad/` links | Name | Filters to `ipad*` slugs |
| `mac.py` | `MacScraper` | `/shop/buy-mac/` links | ConfigKey | Spec extraction (Chip, CPU, GPU, Memory, Storage); filters out displays |
| `watch.py` | `WatchScraper` | `/shop/goto/buy_watch/` | ConfigKey | Enriches names with case size/material from bootstrap dimensions |
| `airpods.py` | `AirPodsScraper` | `/shop/goto/buy_airpods/` | Name or ConfigKey | Auto-selected based on data |
| `tvhome.py` | `TVHomeScraper` | `/shop/goto/buy_tv/` + `/buy_homepod/` | Name | Two URL patterns; overrides `fetch_all_products()` |

#### Mac Spec Extraction (`mac.py`)

Mac products include hardware specification columns. Specs are extracted from HTML `dimension` elements on the product page, then assigned to products by matching price tiers (lowest price → lowest spec). The extraction handles:
- Chip: M1/M2/M3/M4 with Pro/Max/Ultra variants
- CPU/GPU core counts
- Neural Engine cores
- Unified memory (GB)
- Storage (GB/TB)

### Post-Processing

#### Color Consolidation (`smart_consolidate_colors.py`)

Groups products that differ only by color into a single row:

1. Clean color words from product name → base product identity
2. Group by `(base_name, price)` — same product at same price = color variant
3. Mac products additionally group by spec columns when available
4. Output adds `Available_Colors`, `Color_Variants`, and `SKU_Variants` columns

#### JSON Conversion (`convert_to_json.py`)

Converts CSV to structured JSON for the web frontend:
- Fetches USD/TWD exchange rate from Cathay Bank (with fallback to cached/default rate)
- Calculates price difference percentage between US and TW
- Prefers consolidated CSV, falls back to merged CSV
- Outputs to `src/data/` directory

### Output Data Formats

#### Merged CSV (all products)
```csv
SKU,Price_US,Price_TW,PRODUCT_NAME
MG7K4,999.0,34900.0,iPhone 17 Pro 256GB Silver
```

Mac adds spec columns:
```csv
SKU,Chip,CPU_Cores,GPU_Cores,Neural_Engine,Memory,Storage,Price_US,Price_TW,PRODUCT_NAME
```

#### Consolidated CSV (after color merging)
```csv
PRODUCT_NAME,Price_US,Price_TW,Available_Colors,Color_Variants,SKU_Variants
iPhone 17 Pro 256GB,999.0,34900.0,"Silver, Deep Blue, Cosmic Orange",3,"MG7K4, MG7L4, MG7M4"
```

#### JSON (for web frontend)
```json
{
  "metadata": {
    "lastUpdated": "2026-03-27T...",
    "exchangeRates": {"USD": 1.0, "TWD": 31.5},
    "regions": ["US", "TW"],
    "productType": "iphone",
    "totalProducts": 64
  },
  "products": [
    {
      "SKU": "MG7K4",
      "Price_US": 999.0,
      "Price_TW": 34900.0,
      "PRODUCT_NAME": "iPhone 17 Pro 256GB Silver",
      "price_difference_percent": 0.8,
      "product_type": "iphone"
    }
  ]
}
```

## Frontend Architecture

### Core Components

- **Settings Panel**: Exchange rate, foreign transaction fee, local storage persistence
- **Price Summary Cards**: Product count, average price difference, last updated
- **Product Table**: Responsive, searchable, sortable, color-coded price differences
- **Theme System**: Light/dark mode with system preference detection

### Key Files
- `src/index.html` — Single-page app structure
- `src/js/main.js` — All client-side logic
- `src/scss/` — Custom Bootstrap theming
- `src/data/` — Generated JSON data (not committed)
- `manifest.json` — PWA support

## Testing

### Unit Tests (`test_scrapers.py`)

| Test Class | What It Tests |
|-----------|---------------|
| `TestSharedConfiguration` | REGIONS structure, reference region |
| `TestSKUUtilities` | Part number suffix stripping |
| `TestDebugPrint` | Debug output on/off |
| `TestModelDiscoveryFallback` | Falls back to DEFAULT_MODELS on 404 |
| `TestMergeProductData` | Name/ConfigKey merge, price preservation, orphan detection, all scrapers produce same format |
| `TestAlignmentReport` | Orphan detection, completeness warnings, balanced/imbalanced region counts |
| `TestMacSpecExtraction` | Chip/memory/storage regex extraction |
| `TestEndToEndIntegration` | (network) Dynamic model discovery, real data fetch, cross-region name alignment ≥90%, minimum product counts |
| `TestConvertToJson` | CSV→JSON conversion and structure |
| `TestFileOutputs` | Existing CSV file structure validation |
| `TestColorConsolidation` | Color extraction, name cleaning, variant merging, price-based separation |

**Network tests use dynamic model discovery** — no hardcoded product URLs.
Tests remain valid when Apple refreshes the product lineup.

### E2E Tests (`e2e/`)
- Playwright: Chromium, Firefox, WebKit, Mobile Chrome (Pixel 5)
- 15s timeout, 2 retries, screenshots/video on failure

## CI/CD Pipeline

`.github/workflows/scrape-and-deploy.yml`:
- **Triggers**: daily at midnight UTC, push to main, manual dispatch
- **Steps**: checkout → Python setup → pip install → run all scrapers → consolidate colors → convert to JSON → Node setup → npm ci → Vite build → deploy to GitHub Pages
- **Build env**: `VITE_APP_BASE_URL=/apple-store-scrape/`

## Extensibility

### Adding a New Region
Update `REGIONS` in `scraper_base.py` — all scrapers pick it up automatically.

### Adding a New Product Category
1. Create scraper class inheriting from `AppleStoreScraper`
2. Implement `get_models()` and `build_product_url()`
3. Optionally override `post_process_products()` for enrichment
4. Add to `smart_consolidate_colors.py` PRODUCTS list
5. Add to `convert_to_json.py` main function
6. Add to GitHub Actions workflow
7. Add tests

## Known Edge Cases

- **Non-breaking spaces (U+00A0)**: TW Apple pages sometimes use these instead of regular spaces in product names. The framework normalizes them before merge.
- **Bootstrap price location**: Some pages store prices in `mainDisplayValues.prices` instead of `displayValues.prices`. The framework checks both.
- **Missing partNumber**: Mac bootstrap products use `btrOrFdPartNumber` instead of `partNumber`. The framework tries multiple field names.
- **Locale-dependent page titles**: TW page titles include Chinese prefixes ("購買") and region suffixes ("(台灣)"). The framework strips these for fallback name extraction.
- **Model discovery noise**: Landing pages may contain links to non-product pages (carrier-offers, accessories, displays). Each scraper filters discovery results.
