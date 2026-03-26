"""
Shared scraping framework for Apple Store product scrapers.

All product-specific scrapers (iphone.py, ipad.py, etc.) inherit from
AppleStoreScraper to avoid duplicating extraction, merging, and I/O logic.
"""

import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import re
import os


# ==================== SHARED CONFIGURATION ====================

REGIONS = {
    "": ["US", "USD", "en-us", "$"],
    "tw": ["TW", "TWD", "zh-tw", "NT$"],
    # "jp": ["JP", "JPY", "ja-jp", "¥"],
    # "uk": ["UK", "GBP", "en-gb", "£"],
    # "au": ["AU", "AUD", "en-au", "A$"],
    # "ca": ["CA", "CAD", "en-ca", "C$"],
    # "de": ["DE", "EUR", "de-de", "€"],
    # "fr": ["FR", "EUR", "fr-fr", "€"],
}

REFERENCE_REGION = list(REGIONS.keys())[0]
REQUEST_DELAY = 1
DEBUG = os.environ.get('SCRAPER_DEBUG', '').lower() in ('1', 'true', 'yes')


def debug_print(message):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(f"[DEBUG] {message}")


# ==================== SKU UTILITIES ====================

def strip_region_suffix(part_number):
    """
    Strip region-specific suffix from a part number to get the base SKU.

    Apple part numbers follow the pattern: BASE + REGION_SUFFIX
    e.g. MYW23LL/A (US) and MYW23FE/A (TW) share base SKU MYW23.

    Examples:
        "MYW23LL/A" -> "MYW23"
        "MYW23FE/A" -> "MYW23"
        "MYW23/A"   -> "MYW23"
        "MYW23"     -> "MYW23"
    """
    if not part_number:
        return part_number
    result = re.sub(r'[A-Z]{2}/[A-Z]$', '', part_number)
    result = re.sub(r'/[A-Z]$', '', result)
    return result


# ==================== PRODUCT EXTRACTION ====================

def extract_products_from_metrics(soup, region_code):
    """
    Strategy 1: Extract products from the <script id="metrics"> JSON block.

    This is the standard data source on most Apple Store buy pages.
    Returns a list of product dicts or an empty list on failure.
    """
    region_display = REGIONS.get(region_code, ["Unknown"])[0]
    json_script = soup.find('script', {'type': 'application/json', 'id': 'metrics'})
    if not json_script:
        return []

    try:
        json_data = json.loads(json_script.string)
        products = json_data.get('data', {}).get('products', [])
        if not products:
            return []

        debug_print(f"Found {len(products)} products via metrics for region {region_display}")
        result = []
        for product in products:
            sku = product.get("sku", "")
            part_number = product.get("partNumber", "")
            base_sku = strip_region_suffix(part_number) if part_number else sku

            result.append({
                "SKU": base_sku,
                "OriginalSKU": sku or part_number,
                "Name": product.get("name", ""),
                "Price": product.get("price", {}).get("fullPrice"),
                "Region": region_display,
                "Region_Code": region_code,
                "PartNumber": part_number,
            })
        return result

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        debug_print(f"Error parsing metrics JSON: {e}")
        return []


def extract_products_from_bootstrap(soup, region_code):
    """
    Strategy 2: Extract products from window.PRODUCT_SELECTION_BOOTSTRAP.

    Some Apple Store pages (especially Watch and configurable products)
    embed product data in a JS variable instead of the metrics script.
    Returns a list of product dicts or an empty list on failure.
    """
    region_display = REGIONS.get(region_code, ["Unknown"])[0]

    script_content = None
    for script in soup.find_all('script'):
        if script.string and 'window.PRODUCT_SELECTION_BOOTSTRAP' in script.string:
            script_content = script.string
            break

    if not script_content:
        return []

    try:
        key_index = script_content.find('productSelectionData:')
        if key_index == -1:
            return []

        start_index = script_content.find('{', key_index)
        if start_index == -1:
            return []

        # Extract JSON by balanced brace counting.
        # Note: this can fail on strings containing literal braces,
        # but it works for Apple's current page structure.
        brace_count = 0
        json_str = ""
        for i in range(start_index, len(script_content)):
            char = script_content[i]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            json_str += char
            if brace_count == 0:
                break

        if not json_str:
            return []

        bootstrap_data = json.loads(json_str)
        products = bootstrap_data.get('products', [])
        # Prices can be in displayValues.prices OR mainDisplayValues.prices
        prices_map = bootstrap_data.get('displayValues', {}).get('prices', {})
        if not prices_map:
            prices_map = bootstrap_data.get('mainDisplayValues', {}).get('prices', {})

        if not products:
            return []

        debug_print(f"Found {len(products)} products via bootstrap for region {region_display}")

        # Fallback page title for name extraction.
        # Titles differ by locale: "Buy AirPods Pro 3 - Apple" (US) vs
        # "購買 AirPods Pro 3 - Apple (台灣)" (TW). We strip locale-specific
        # prefixes and suffixes to get a consistent product name.
        page_title_tag = soup.find('title')
        fallback_name = ""
        if page_title_tag:
            fallback_name = page_title_tag.text
            # Strip " - Apple" or " - Apple (region)" suffix
            fallback_name = re.split(r'\s*-\s*Apple', fallback_name)[0].strip()
            # Strip common locale buy-prefixes
            for prefix in ['Buy ', '購買 ', 'Comprar ', 'Acheter ', 'Kaufen ']:
                if fallback_name.startswith(prefix):
                    fallback_name = fallback_name[len(prefix):]
                    break
            fallback_name = fallback_name.strip()

        result = []
        for product in products:
            # Part number: try multiple fields (Mac uses btrOrFdPartNumber instead of partNumber)
            part_number = (product.get('partNumber')
                           or product.get('part')
                           or product.get('btrOrFdPartNumber')
                           or '')

            base_part_number = product.get('basePartNumber')
            base_sku = base_part_number if base_part_number else strip_region_suffix(part_number)

            # Price lookup — Apple uses different key names across pages
            # Price and config key
            price_key = (product.get('priceKey')
                         or product.get('fullPrice')
                         or product.get('price'))
            price_val = _parse_bootstrap_price(prices_map, price_key)

            # priceKey is a configuration identifier shared across regions
            # (e.g. "m4-10-10", "13inch-midnight-10-10") — used as merge key
            config_key = price_key or ''

            # Name extraction
            # familyType is often generic ("MacBook Pro") or empty for bootstrap.
            # Subclasses can improve names via post_process_products().
            family = product.get('familyType', '')
            if family and not family.islower():
                name = family
            else:
                name = fallback_name or "Unknown Product"

            # Skip products with no usable identifier at all
            if not base_sku and not part_number and not name:
                continue

            result.append({
                "SKU": base_sku or part_number or f"unknown-{len(result)}",
                "OriginalSKU": part_number,
                "Name": name,
                "ConfigKey": config_key,
                "Price": price_val,
                "Region": region_display,
                "Region_Code": region_code,
                "PartNumber": part_number,
                "_bootstrap_product": product,  # preserved for post-processing hooks
            })
        return result

    except (json.JSONDecodeError, KeyError, TypeError) as e:
        debug_print(f"Error parsing bootstrap JSON: {e}")
        return []


def _parse_bootstrap_price(prices_map, price_key):
    """Extract numeric price from bootstrap displayValues.prices map."""
    if not price_key or not prices_map:
        return None
    price_info = prices_map.get(price_key, {})
    curr_price = price_info.get('currentPrice', {})
    raw_amount = curr_price.get('raw_amount')
    if raw_amount:
        try:
            return float(str(raw_amount).replace(',', ''))
        except (ValueError, TypeError):
            pass
    return None


def fetch_product_page(url, region_code):
    """
    Fetch an Apple Store product page and extract products using
    the dual-strategy approach (metrics first, then bootstrap fallback).

    Returns a list of product dicts.
    """
    time.sleep(REQUEST_DELAY)
    region_display = REGIONS.get(region_code, ["Unknown"])[0]
    debug_print(f"Fetching products from {url} for region {region_display}")

    try:
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            debug_print(f"Failed to retrieve {url}. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Try metrics first (more structured, preferred)
        products = extract_products_from_metrics(soup, region_code)
        if products:
            return products

        # Fallback to bootstrap
        debug_print("Metrics strategy found no products, trying bootstrap")
        products = extract_products_from_bootstrap(soup, region_code)
        if products:
            return products

        debug_print(f"No products found at {url}")
        return []

    except requests.RequestException as e:
        debug_print(f"Network error fetching {url}: {e}")
        return []
    except Exception as e:
        debug_print(f"Unexpected error fetching {url}: {e}")
        return []


# ==================== MODEL DISCOVERY ====================

def discover_models(region_code, landing_url, link_pattern, default_models):
    """
    Discover available models from an Apple Store landing page.

    Args:
        region_code: Region code (e.g. "", "tw")
        landing_url: Full URL of the landing/buy page
        link_pattern: Substring to match in href (e.g. '/shop/buy-ipad/')
        default_models: Fallback list if discovery fails

    Returns:
        list of model slugs (e.g. ["ipad-pro", "ipad-air"])
    """
    try:
        response = requests.get(landing_url, timeout=30)
        if response.status_code != 200:
            debug_print(f"Cannot access {landing_url}, using default model list")
            return default_models

        soup = BeautifulSoup(response.text, 'html.parser')
        models = []

        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if link_pattern in href:
                parts = href.split(link_pattern)
                if len(parts) > 1:
                    model = parts[1].split('?')[0].split('#')[0]
                    if model:
                        models.append(model)

        unique_models = list(set(models))
        if unique_models:
            debug_print(f"Discovered models: {', '.join(unique_models)}")
            return unique_models

        debug_print(f"No models found at {landing_url}, using defaults")
        return default_models

    except Exception as e:
        debug_print(f"Error discovering models: {e}, using defaults")
        return default_models


def discover_models_from_goto(region_code, landing_url, goto_pattern, default_models):
    """
    Discover models from /shop/goto/ links on marketing pages.

    Args:
        region_code: Region code
        landing_url: Marketing page URL (e.g. apple.com/airpods/)
        goto_pattern: Pattern in href (e.g. '/shop/goto/buy_airpods/')
        default_models: Fallback list

    Returns:
        list of model slugs with underscores replaced by hyphens
    """
    try:
        response = requests.get(landing_url, timeout=30)
        if response.status_code != 200:
            debug_print(f"Cannot access {landing_url}, using default model list")
            return default_models

        soup = BeautifulSoup(response.text, 'html.parser')
        models = []

        for link in soup.find_all('a', href=True):
            href = link.get('href')
            if goto_pattern in href:
                parts = href.split(goto_pattern)
                if len(parts) > 1:
                    model_raw = parts[1].split('?')[0].split('#')[0]
                    # Apple uses underscores in goto links but hyphens in store URLs
                    model = model_raw.replace('_', '-')
                    # Strip sub-configurations (e.g. /with_active_noise_cancellation)
                    if '/' in model:
                        model = model.split('/')[0]
                    if model:
                        models.append(model)

        unique_models = list(set(models))
        if unique_models:
            debug_print(f"Discovered models: {', '.join(unique_models)}")
            return unique_models

        debug_print(f"No models found at {landing_url}, using defaults")
        return default_models

    except Exception as e:
        debug_print(f"Error discovering models: {e}, using defaults")
        return default_models


# ==================== DATA MERGING ====================

def merge_product_data(product_data, extra_columns=None):
    """
    Merge product data from all regions using Name-based matching.

    Apple uses different part numbers per region for the same product,
    so we match by product Name (which is identical across regions in
    the metrics JSON). The reference region's SKU is kept for identification.

    Args:
        product_data: list of product dicts from fetch_product_page()
        extra_columns: optional list of additional columns to preserve
                       from the reference region (e.g. ["Chip", "Memory", "Storage"])

    Returns:
        DataFrame with columns: SKU, [extra_columns], Price_US, Price_TW, ..., PRODUCT_NAME
    """
    df = pd.DataFrame(product_data)
    if df.empty:
        debug_print("No product data to merge!")
        return pd.DataFrame()

    # Remove _bootstrap_product helper column if present
    if '_bootstrap_product' in df.columns:
        df = df.drop(columns=['_bootstrap_product'])

    # Normalize whitespace in Name: Apple uses non-breaking spaces (U+00A0) on some
    # regional pages, which look identical but fail string equality checks.
    if 'Name' in df.columns:
        df['Name'] = df['Name'].str.replace('\u00a0', ' ', regex=False).str.strip()

    # Choose the merge key:
    # - ConfigKey (priceKey from bootstrap) is a configuration identifier shared across
    #   regions (e.g. "m4-10-10"). Available for bootstrap products (Mac, Watch, etc.)
    # - Name is identical across regions for metrics products (iPhone, iPad, TV/Home).
    # Use ConfigKey when all products have a non-empty one; otherwise use Name.
    has_config_key = ('ConfigKey' in df.columns
                      and df['ConfigKey'].notna().all()
                      and (df['ConfigKey'] != '').all())
    merge_key = 'ConfigKey' if has_config_key else 'Name'
    debug_print(f"Merge key: {merge_key}")

    region_dfs = {}
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        region_data = df[df['Region_Code'] == region_code].copy()
        region_data = region_data.drop_duplicates(subset=merge_key)

        region_data.rename(columns={
            'SKU': f'SKU_{region_display}',
            'Price': f'Price_{region_display}',
            'PartNumber': f'PartNumber_{region_display}',
        }, inplace=True)

        region_dfs[region_code] = region_data

    ref_region = REFERENCE_REGION
    ref_display = REGIONS[ref_region][0]

    if ref_region not in region_dfs or region_dfs[ref_region].empty:
        debug_print(f"Reference region {ref_display} has no data!")
        return pd.DataFrame()

    # When merging by ConfigKey, rename Name per region so we can look up the
    # reference region's name later for PRODUCT_NAME. When merging by Name,
    # keep it as-is since it IS the merge key.
    if merge_key == 'ConfigKey':
        for region_code, region_info in REGIONS.items():
            region_display = region_info[0]
            if region_code in region_dfs and 'Name' in region_dfs[region_code].columns:
                region_dfs[region_code] = region_dfs[region_code].rename(
                    columns={'Name': f'Name_{region_display}'})

    # Build base columns from reference region
    base_cols = [merge_key, f'SKU_{ref_display}', f'Price_{ref_display}']
    if merge_key == 'ConfigKey':
        base_cols.append(f'Name_{ref_display}')
    if extra_columns:
        base_cols.extend([c for c in extra_columns if c in region_dfs[ref_region].columns])
    available_base = [c for c in base_cols if c in region_dfs[ref_region].columns]
    merged_df = region_dfs[ref_region][available_base].copy()

    # Merge other regions on Name
    for region_code, region_df in region_dfs.items():
        if region_code == ref_region:
            continue
        region_display = REGIONS[region_code][0]
        cols = [merge_key, f'Price_{region_display}']
        available = [c for c in cols if c in region_df.columns]
        merged_df = pd.merge(merged_df, region_df[available], on=merge_key, how='outer')

    # Fill missing prices with 0
    for region_code, region_info in REGIONS.items():
        region_display = region_info[0]
        price_col = f'Price_{region_display}'
        if price_col in merged_df.columns:
            merged_df[price_col] = merged_df[price_col].fillna(0)

    # Rename reference SKU column and add PRODUCT_NAME
    merged_df = merged_df.rename(columns={f'SKU_{ref_display}': 'SKU'})

    # PRODUCT_NAME: use Name column if merge key was ConfigKey
    if merge_key == 'ConfigKey':
        # For ConfigKey merges, we need to look up the Name from the reference region data
        name_col = f'Name_{ref_display}'
        if name_col in region_dfs[ref_region].columns:
            # Build ConfigKey -> Name mapping from reference region
            ref_df = region_dfs[ref_region]
            key_to_name = dict(zip(ref_df[merge_key], ref_df[name_col]))
            merged_df['PRODUCT_NAME'] = merged_df[merge_key].map(key_to_name).fillna(merged_df[merge_key])
        else:
            merged_df['PRODUCT_NAME'] = merged_df[merge_key]
        # Drop ConfigKey from output
        if merge_key in merged_df.columns:
            merged_df = merged_df.drop(columns=[merge_key])
    else:
        # Name was the merge key — just rename it
        merged_df = merged_df.rename(columns={merge_key: 'PRODUCT_NAME'})

    # Fill missing SKU
    if 'SKU' in merged_df.columns:
        merged_df['SKU'] = merged_df['SKU'].fillna('')

    # Build output column order
    output_cols = ['SKU']
    if extra_columns:
        output_cols.extend([c for c in extra_columns if c in merged_df.columns])
    for region_code, region_info in REGIONS.items():
        price_col = f'Price_{region_info[0]}'
        if price_col in merged_df.columns:
            output_cols.append(price_col)
    output_cols.append('PRODUCT_NAME')

    # Fill any remaining NaN in extra columns
    if extra_columns:
        for col in extra_columns:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].fillna('')

    available_output = [c for c in output_cols if c in merged_df.columns]
    result = merged_df[available_output].copy()

    # Report alignment stats
    _report_alignment(result)

    return result


def _report_alignment(df):
    """Report cross-region alignment stats. Only prints details when there are orphans."""
    if df.empty:
        return

    price_cols = [c for c in df.columns if c.startswith('Price_')]
    if len(price_cols) < 2:
        return

    total = len(df)
    all_aligned = df[(df[price_cols] > 0).all(axis=1)]
    aligned_count = len(all_aligned)

    # Only print details if there are orphans
    if aligned_count < total:
        print(f"  WARNING: {total - aligned_count} orphan(s) out of {total} products")
        for col in price_cols:
            region = col.replace('Price_', '')
            orphans = df[df[col] == 0]
            if not orphans.empty:
                for _, row in orphans.head(5).iterrows():
                    print(f"    Missing {region}: {row.get('PRODUCT_NAME', '?')}")
                if len(orphans) > 5:
                    print(f"    ... and {len(orphans) - 5} more")


def validate_completeness(products_by_region):
    """
    Validate that scraping produced a reasonable number of products per region.

    Args:
        products_by_region: dict mapping region_code -> list of product dicts

    Returns:
        dict with validation results per region
    """
    results = {}
    counts = {code: len(prods) for code, prods in products_by_region.items()}

    for code, count in counts.items():
        region_name = REGIONS.get(code, ["Unknown"])[0]
        results[region_name] = {
            'count': count,
            'warning': None,
        }
        if count == 0:
            results[region_name]['warning'] = f"NO products found for {region_name}!"
            print(f"WARNING: {results[region_name]['warning']}")

    # Cross-region count comparison: regions should have similar product counts
    if len(counts) >= 2:
        max_count = max(counts.values())
        for code, count in counts.items():
            region_name = REGIONS.get(code, ["Unknown"])[0]
            if max_count > 0 and count < max_count * 0.5:
                msg = (f"{region_name} has only {count} products vs {max_count} max — "
                       f"possible incomplete scrape ({count/max_count*100:.0f}% of largest region)")
                results[region_name]['warning'] = msg
                print(f"WARNING: {msg}")

    return results


# ==================== SCRAPER BASE CLASS ====================

class AppleStoreScraper:
    """
    Base class for all Apple Store product scrapers.

    Subclasses must implement:
        - product_name: str property (e.g. "iPhone", "iPad")
        - output_file: str property (e.g. "iphone_products_merged.csv")
        - get_models() -> list of model slugs
        - build_product_url(model, region_code) -> URL string

    Subclasses may override:
        - post_process_products(products, soup) -> products
          to add product-specific enrichment (e.g. Mac specs)
        - extra_columns -> list of additional columns to preserve in merge
    """

    product_name = ""
    output_file = ""
    extra_columns = None

    def get_models(self):
        """Return list of model slugs to scrape."""
        raise NotImplementedError

    def build_product_url(self, model, region_code):
        """Build the full URL for a model + region."""
        raise NotImplementedError

    def post_process_products(self, products, soup):
        """Optional hook for product-specific enrichment. Override in subclass."""
        return products

    def fetch_all_products(self):
        """Fetch products for all models from all regions."""
        models = self.get_models()
        debug_print(f"Models to scrape: {', '.join(models)}")

        all_products = []
        for model in models:
            for region_code in REGIONS.keys():
                url = self.build_product_url(model, region_code)

                # Use the shared dual-strategy extraction
                time.sleep(REQUEST_DELAY)
                region_display = REGIONS.get(region_code, ["Unknown"])[0]
                debug_print(f"Fetching products from {url} for region {region_display}")

                try:
                    response = requests.get(url, timeout=30)
                    if response.status_code != 200:
                        debug_print(f"Failed to retrieve {url}. Status code: {response.status_code}")
                        continue

                    soup = BeautifulSoup(response.text, 'html.parser')

                    products = extract_products_from_metrics(soup, region_code)
                    if not products:
                        debug_print("Metrics found no products, trying bootstrap")
                        products = extract_products_from_bootstrap(soup, region_code)

                    if products:
                        products = self.post_process_products(products, soup)

                    all_products.extend(products)

                except requests.RequestException as e:
                    debug_print(f"Network error fetching {url}: {e}")
                except Exception as e:
                    debug_print(f"Unexpected error fetching {url}: {e}")

        return all_products

    def merge(self, product_data):
        """Merge product data from all regions."""
        return merge_product_data(product_data, extra_columns=self.extra_columns)

    def run(self):
        """Execute the full scraping pipeline: fetch, merge, save."""
        all_products = self.fetch_all_products()

        # Completeness check
        products_by_region = {}
        for p in all_products:
            rc = p.get('Region_Code', '')
            products_by_region.setdefault(rc, []).append(p)
        validate_completeness(products_by_region)

        # Merge (includes alignment report)
        merged_data = self.merge(all_products)

        merged_data.to_csv(self.output_file, index=False, encoding='utf-8-sig')

        # Summary line
        total = len(merged_data)
        price_cols = [c for c in merged_data.columns if c.startswith('Price_')]
        aligned = len(merged_data[(merged_data[price_cols] > 0).all(axis=1)]) if price_cols else total
        region_counts = ', '.join(
            f"{REGIONS[rc][0]}={int((merged_data[f'Price_{REGIONS[rc][0]}'] > 0).sum())}"
            for rc in REGIONS if f'Price_{REGIONS[rc][0]}' in merged_data.columns
        )
        print(f"{self.product_name}: {total} products, {aligned}/{total} aligned ({region_counts}) -> {self.output_file}")

        return merged_data
