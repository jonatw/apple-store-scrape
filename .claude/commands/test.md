# Run Tests

Run the full test suite and analyze results.

---

## Steps

### 1. Quick Tests (no network)
```bash
SKIP_NETWORK_TESTS=1 python3 test_scrapers.py
```

### 2. If all quick tests pass
- Report the number of tests passed
- Ask the user whether to proceed with network tests

### 3. If any test fails
- List each failing test name and error message
- Read the relevant test code and the production code being tested
- Analyze root cause (production bug vs outdated test)
- Suggest fixes, but **do NOT modify test files automatically**

### 4. Network Tests (requires user confirmation)
```bash
python3 -m unittest test_scrapers.TestEndToEndIntegration -v
```

### 5. Build Verification
```bash
npm run build
```

## Rules

- When tests fail, fix production code first — never modify tests without user approval
- Network tests hit Apple's live website — confirm before running
- E2E tests require a separate dev server — not included in this command
