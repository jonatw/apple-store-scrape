---
name: apple-color-fix
description: Fix color variant consolidation issues in Apple product scrapers. Use when color variants (Pink, Teal, Space Black, Silver, etc.) are not properly merged for same-spec products. Applies bulletproof consolidation logic across iPhone, iPad, Mac, AirPods, Watch, and TV product lines.
---

# Apple Color Fix

This skill provides systematic diagnosis and repair of color variant consolidation issues in the Apple product scraping system.

## Problem

Apple products often come in multiple colors (Pink, Teal, Silver, Space Black, etc.) with identical specs and prices. These should be consolidated into single products without color suffixes for clean price comparison.

**Example Issue:**
```
❌ BEFORE: "iPhone 16 128GB Pink", "iPhone 16 128GB Teal", "iPhone 16 128GB Ultramarine" 
✅ AFTER:  "iPhone 16 128GB"
```

## Diagnostic Workflow

1. **Identify affected products** - Check static JSON data for color variants
2. **Verify consolidation logic** - Test `robust_consolidation.py` on sample data  
3. **Apply systematic fix** - Update all product line scrapers
4. **Validate deployment** - Confirm fixes work in production

## Implementation

Use the diagnostic script to identify issues:

```bash
python scripts/diagnose_color_issues.py --product [iphone|ipad|mac|airpods|watch|tvhome]
```

Apply the systematic fix:

```bash
python scripts/apply_color_fix.py --all-products
```

## Reference Files

- **Technical Details**: See [references/consolidation-logic.md](references/consolidation-logic.md) for robust_consolidation.py algorithm
- **Product Patterns**: See [references/product-patterns.md](references/product-patterns.md) for color naming patterns across Apple products
- **Testing Guide**: See [references/testing-procedures.md](references/testing-procedures.md) for validation procedures