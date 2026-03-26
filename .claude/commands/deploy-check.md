# Deploy Check

Pre-deployment checklist to verify all configurations are consistent.

---

## Checks

### 1. Data Integrity
- Confirm all `src/data/*.json` files exist and are non-empty
- Confirm each JSON file contains valid product data
- Confirm `exchange_rate.json` exists and the rate is reasonable (USD/TWD typically 28-35)

### 2. Build Verification
```bash
npm run build
```
- Confirm `dist/index.html` exists
- Confirm all JSON data was copied to `dist/`
- Confirm no missing static assets in `dist/`

### 3. GitHub Actions Consistency
- Read `.github/workflows/scrape-and-deploy.yml`
- Confirm all scrapers are listed in workflow steps
- Confirm `VITE_APP_BASE_URL` is set correctly
- Confirm Python and Node.js versions match local development

### 4. Tests Pass
```bash
SKIP_NETWORK_TESTS=1 python3 test_scrapers.py
```
- Confirm all quick tests pass

### 5. Package Versions
- Does `package.json` version need updating?
- Are there any outdated dependencies?

## Output Format

```
## Deploy Check Results

### [FAIL] Blocks Deployment
- ...

### [WARN] Should Fix
- ...

### [PASS] All Good
- ...
```
