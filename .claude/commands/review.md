# Code Review

Perform a full code review on current changes (`git diff main`).
Review based on this project's architecture and known risk areas.

---

## Architecture Context

- **Data flow**: Apple Store web pages → Python scrapers (CSV) → color consolidation → JSON conversion + exchange rate → Vite build → GitHub Pages
- **All scrapers enforce 1-second delay** between requests — never remove rate limiting
- **Apple Store HTML structure changes frequently** — scrapers need fallback mechanisms
- **CI/CD**: GitHub Actions runs full pipeline daily

---

## 1. Scraper Quality

### Network Requests
- Is `time.sleep(1)` rate limiting preserved?
- Is there proper error handling (HTTP errors, timeouts, empty responses)?
- Do new requests calls set a timeout?
- Is there a User-Agent header?

### Data Parsing
- Are BeautifulSoup selectors too fragile (relying on specific class names)?
- Are there fallback mechanisms? (reference existing scraper fallback defaults)
- Do new scrapers follow the `REGIONS` dict convention?
- Is product name standardization consistent?

### Output Format
- Does CSV output maintain `Product, USD Price, TWD Price` column format?
- Are prices numeric (not strings with currency symbols)?
- Does file naming follow `{product}_products.csv` convention?

---

## 2. Data Pipeline

### smart_consolidate_colors.py
- Could new color merging logic incorrectly merge different products?
- Does `ignored_words` list need updating?
- Is the "keep lowest price" logic preserved?

### convert_to_json.py
- Does CSV → JSON conversion maintain data integrity?
- Is there a fallback when Cathay Bank exchange rate page is unreachable?
- Is the JSON output path correct (`src/data/`)?

---

## 3. Frontend

- Any XSS risk from dynamically inserting unsanitized data?
- Does dark/light theme toggle still work?
- Is mobile responsiveness broken?
- Do new UI elements use Bootstrap 5 components?

---

## 4. Tests

- Do new features have corresponding test cases?
- Risk of breaking existing tests?
- Can network tests be skipped with `SKIP_NETWORK_TESTS=1`?

---

## 5. CI/CD

- Does `.github/workflows/scrape-and-deploy.yml` need updating?
- Are new scrapers added to workflow steps?
- Is `VITE_APP_BASE_URL` set correctly?

---

## Output Format

```
## Code Review Results

### FAIL — Must Fix
- [Description] (file:line)

### WARN — Suggested Improvements
- [Description] (file:line)

### PASS — Good Practices
- [Positive observations]

### Verdict
[Ready to merge / Needs changes / Do not merge] — reason
```
