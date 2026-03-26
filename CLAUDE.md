# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Apple Store Price Compare** is a web scraping + comparison tool that scrapes Apple product prices across regions (US/Taiwan), consolidates color variants, converts data to JSON, and serves a responsive comparison website.

**Live Site:** https://jonatw.github.io/apple-store-scrape/

**Tech Stack:**
- **Scrapers:** Python 3.10+ with requests + BeautifulSoup4 + pandas
- **Frontend:** Vanilla JavaScript + Bootstrap 5 + Vite (ES module)
- **Testing:** Python unittest (scrapers) + Playwright (E2E)
- **CI/CD:** GitHub Actions (daily scrape + deploy to GitHub Pages)

## Essential Development Commands

### Setup
```bash
# Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Node.js dependencies
npm install

# Playwright browsers (for E2E)
npx playwright install
```

### Scraping Pipeline
```bash
# Run full pipeline: scrape all products → consolidate colors → convert to JSON
npm run scrape

# Individual scrapers
python3 iphone.py
python3 ipad.py
python3 mac.py
python3 watch.py
python3 airpods.py
python3 tvhome.py

# Post-processing
python3 smart_consolidate_colors.py   # Merge color variants
python3 convert_to_json.py            # CSV → JSON + fetch exchange rate
```

### Testing
```bash
# Quick tests only (skip network tests) — use this before/after changes
SKIP_NETWORK_TESTS=1 python3 test_scrapers.py

# Full Python test suite (includes network tests hitting apple.com)
npm run test

# Network integration tests only
npm run test-network

# E2E tests
npm run test:e2e
npm run test:e2e:local
```

### Frontend Development
```bash
npm run dev       # Start Vite dev server (opens browser)
npm run build     # Production build → dist/
npm run preview   # Preview production build
```

## Architecture Overview

### Data Pipeline Flow
```
Apple Store websites (US/TW)
  ↓ (Python scrapers with 1s rate limiting)
Per-product CSV files (*_products_merged.csv)
  ↓ (smart_consolidate_colors.py)
Consolidated CSV files (*_products_consolidated.csv) — color variants merged
  ↓ (convert_to_json.py + Cathay Bank exchange rate)
JSON files in src/data/ (iphone_data.json, ipad_data.json, ..., exchange_rate.json)
  ↓ (Vite build)
Static site in dist/ → GitHub Pages
```

### Shared Scraper Framework (`scraper_base.py`)

All 6 product scrapers inherit from a shared base class. This eliminates code
duplication and ensures consistent behavior:

- **`REGIONS`** — shared region configuration (US + TW), single source of truth
- **`extract_products_from_metrics()`** — Strategy 1: extract from `<script id="metrics">` JSON
- **`extract_products_from_bootstrap()`** — Strategy 2: extract from `window.PRODUCT_SELECTION_BOOTSTRAP`
- **`fetch_product_page()`** — dual-strategy extraction with error handling and rate limiting
- **`discover_models()` / `discover_models_from_goto()`** — dynamic model discovery from landing pages
- **`merge_product_data()`** — cross-region merge with automatic key selection and alignment reporting
- **`validate_completeness()`** — warns when a region has far fewer products than expected
- **`AppleStoreScraper`** — base class with `run()` pipeline

### Product Scrapers
| File | Class | Products | Notes |
|------|-------|----------|-------|
| `iphone.py` | `IPhoneScraper` | iPhone models | Filters discovery to `iphone*` slugs |
| `ipad.py` | `IPadScraper` | iPad models | Filters discovery to `ipad*` slugs |
| `mac.py` | `MacScraper` | Mac lineup | Extra spec columns (Chip, Memory, Storage); filters out displays/accessories |
| `watch.py` | `WatchScraper` | Apple Watch | Enriches names with case size/material from bootstrap dimensions |
| `airpods.py` | `AirPodsScraper` | AirPods | Uses goto-link discovery pattern |
| `tvhome.py` | `TVHomeScraper` | Apple TV, HomePod | Two product categories; overrides `fetch_all_products()` |

### Key Design Decisions

**Cross-region matching uses two strategies depending on data source:**

- **Metrics products** (iPhone, iPad, TV/Home): matched by `Name`. Apple's metrics JSON
  uses identical English product names across all regions. Unicode non-breaking spaces
  (U+00A0) on some regional pages are normalized to regular spaces before matching.

- **Bootstrap products** (Mac, Watch, some AirPods): matched by `ConfigKey` (the `priceKey`
  field from bootstrap data, e.g. `m4-10-10`, `13inch-midnight-10-10`). This is a
  configuration identifier shared across regions. Bootstrap page titles differ by locale
  (e.g. "Buy Mac mini" vs "購買 Mac mini (台灣)") so Name is unreliable here.

The merge function auto-selects the strategy: ConfigKey when all products have one,
Name otherwise.

**Apple uses different part numbers per region.** The same physical product has
different SKUs in US vs TW (e.g. `MG7K4LL/A` vs a completely different number).
SKU-based matching does NOT work. The output CSV keeps the reference region's (US) SKU.

**Dynamic model discovery.** All scrapers discover current models from Apple's landing
pages at runtime. `DEFAULT_MODELS` lists are last-resort fallbacks only used when
Apple's website is completely unreachable.

**Bootstrap price location varies.** Prices may be in `displayValues.prices` or
`mainDisplayValues.prices` — the framework checks both.

**Unified CSV output format:** `SKU, Price_US, Price_TW, PRODUCT_NAME` (Mac adds spec columns).

### Post-Processing
- `smart_consolidate_colors.py` — groups products by (cleaned base name, price), merges color variants into single rows with `Available_Colors` and `Color_Variants` columns
- `convert_to_json.py` — CSV → JSON, fetches USD/TWD exchange rate from Cathay Bank with fallback to cached/default rate

### Frontend (src/)
- `src/index.html` — Single-page app
- `src/js/main.js` — Product filtering, price comparison, theme toggle, PWA support
- `src/scss/` — Custom Bootstrap theming
- `src/data/` — JSON data files (generated, not committed)

### CI/CD Pipeline
- `.github/workflows/scrape-and-deploy.yml`
- Triggers: daily at midnight UTC, push to main, manual dispatch
- Steps: Python scrape → consolidate → JSON convert → Vite build → GitHub Pages deploy
- `VITE_APP_BASE_URL=/apple-store-scrape/` for GitHub Pages path prefix

## Region Configuration

All scrapers share the REGIONS config from `scraper_base.py`:
```python
REGIONS = {
    "": ["US", "USD", "en-us", "$"],
    "tw": ["TW", "TWD", "zh-tw", "NT$"],
}
```
To add a region: update `REGIONS` in `scraper_base.py` (one place, applies to all scrapers).

## Testing Details

### Python Tests (`test_scrapers.py`)
- `TestSharedConfiguration` — REGIONS structure, reference region
- `TestSKUUtilities` — part number suffix stripping
- `TestDebugPrint` — debug output on/off
- `TestModelDiscoveryFallback` — fallback to defaults on network failure
- `TestMergeProductData` — Name/ConfigKey merge, column format, price preservation, orphan detection
- `TestAlignmentReport` — orphan detection, completeness validation, cross-region balance warnings
- `TestMacSpecExtraction` — chip/memory/storage extraction from text
- `TestEndToEndIntegration` — (network) dynamic model discovery, real data fetch, cross-region name alignment ≥90%, per-page product count ≥2
- `TestConvertToJson` — CSV→JSON conversion
- `TestFileOutputs` — existing CSV/consolidated file structure
- `TestColorConsolidation` — color extraction, name cleaning, merge logic

All network tests use **dynamic model discovery** — no hardcoded product URLs.
Tests remain valid when Apple refreshes the product lineup.

### E2E Tests (`e2e/`)
- Playwright with Chromium, Firefox, WebKit, and Mobile Chrome (Pixel 5)
- 15s timeout, 2 retries
- Screenshots/videos on failure

## AI Development Workflow

### Before making any change
1. Run the quick test suite and confirm it passes:
   ```bash
   SKIP_NETWORK_TESTS=1 python3 test_scrapers.py
   ```
2. Read `CLAUDE.md` to understand the area being changed.

### When modifying scrapers
- **Edit `scraper_base.py`** for shared extraction/merge logic. Do NOT duplicate logic in individual scrapers.
- Apple Store HTML structure changes frequently — verify selectors against live pages first.
- Maintain the 1-second rate limiting between requests.
- Bootstrap data structures vary between product types — check `displayValues` vs `mainDisplayValues`, `partNumber` vs `btrOrFdPartNumber`, `priceKey` vs `fullPrice`.
- Watch for Unicode whitespace issues (U+00A0) in cross-region Name comparisons.
- Run network tests after changes: `python3 -m unittest test_scrapers.TestEndToEndIntegration -v`

### When adding a new product category
1. Create a new scraper class inheriting from `AppleStoreScraper`.
2. Implement `get_models()`, `build_product_url()`, and optionally `post_process_products()`.
3. Add to `smart_consolidate_colors.py` PRODUCTS list.
4. Add to `convert_to_json.py` main function.
5. Add to `.github/workflows/scrape-and-deploy.yml`.
6. Add tests.

### When modifying the frontend
- Test with both light and dark themes
- Verify mobile responsiveness (Bootstrap 5 breakpoints)
- Run E2E: `npm run test:e2e:local`

### After making changes
1. Run quick tests again and confirm all pass.
2. If any test fails, fix the production code first. Do not modify tests without user approval.
3. Run `npm run build` to verify the frontend builds successfully.

### When uncertain
- Do not guess at Apple Store HTML structure. Check the live page first.
- Do not assume patterns between product categories — Apple uses different page layouts and data structures.
- If a change requires touching `scraper_base.py`, describe the impact on all scrapers first.
