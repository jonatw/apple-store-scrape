# Run Scrape Pipeline

Execute the full data scraping and processing pipeline.

---

## Steps

### 1. Verify Python Environment
```bash
python3 --version
pip list | grep -E "requests|beautifulsoup4|pandas"
```

### 2. Run All Scrapers
Execute each scraper sequentially:
```bash
python3 iphone.py
python3 ipad.py
python3 mac.py
python3 watch.py
python3 airpods.py
python3 tvhome.py
```

### 3. Verify CSV Output
- Confirm all CSV files were generated
- Each file should have at least 1 data row (excluding header)
- Report product count per file

### 4. Consolidate Color Variants
```bash
python3 smart_consolidate_colors.py
```
- Report product count before vs after consolidation

### 5. Convert to JSON
```bash
python3 convert_to_json.py
```
- Confirm JSON files generated under `src/data/`
- Confirm exchange rate was fetched

### 6. Build Verification
```bash
npm run build
```
- Confirm `dist/` directory was generated
- Confirm JSON data was copied to `dist/`

## Final Report

```
## Scrape Pipeline Results

| Product | CSV Count | After Merge | JSON |
|---------|-----------|-------------|------|
| iPhone  | ...       | ...         | OK/FAIL |
| iPad    | ...       | ...         | OK/FAIL |
| Mac     | ...       | ...         | OK/FAIL |
| Watch   | ...       | ...         | OK/FAIL |
| AirPods | ...       | ...         | OK/FAIL |
| TV/Home | ...       | ...         | OK/FAIL |

Exchange Rate: USD/TWD = ...
Build: OK/FAIL
```
