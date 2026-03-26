#!/usr/bin/env python3
"""
Run the full scraping pipeline: scrape all products in parallel,
consolidate color variants, and convert to JSON.

Used by GitHub Actions and local development (npm run scrape).
"""

import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

SCRAPERS = [
    ("iPhone", "iphone.py"),
    ("iPad", "ipad.py"),
    ("Mac", "mac.py"),
    ("Watch", "watch.py"),
    ("AirPods", "airpods.py"),
    ("TV/Home", "tvhome.py"),
]

POST_STEPS = [
    ("Color consolidation", "smart_consolidate_colors.py"),
    ("JSON conversion", "convert_to_json.py"),
]


def run_script(name, script):
    """Run a Python script and return (name, success, output)."""
    try:
        result = subprocess.run(
            [sys.executable, script],
            capture_output=True, text=True, timeout=300,
        )
        output = result.stdout + result.stderr
        if result.returncode != 0:
            return name, False, output
        # Extract the summary line (last non-empty line from stdout)
        summary = ''
        for line in reversed(result.stdout.strip().splitlines()):
            if line.strip():
                summary = line.strip()
                break
        return name, True, summary
    except subprocess.TimeoutExpired:
        return name, False, f"timed out after 300s"
    except Exception as e:
        return name, False, str(e)


def main():
    print("=" * 60)
    print("Apple Store Scraping Pipeline")
    print("=" * 60)

    # Phase 1: Run all scrapers in parallel
    print(f"\nPhase 1: Scraping ({len(SCRAPERS)} products in parallel)...")
    failures = []

    with ThreadPoolExecutor(max_workers=len(SCRAPERS)) as executor:
        futures = {
            executor.submit(run_script, name, script): name
            for name, script in SCRAPERS
        }
        for future in as_completed(futures):
            name, success, output = future.result()
            if success:
                print(f"  [OK]   {output}")
            else:
                print(f"  [FAIL] {name}")
                print(f"         {output[:200]}")
                failures.append(name)

    if failures:
        print(f"\nWARNING: {len(failures)} scraper(s) failed: {', '.join(failures)}")
        print("Continuing with available data...\n")

    # Phase 2: Post-processing (sequential — each step depends on previous)
    print(f"\nPhase 2: Post-processing...")
    for name, script in POST_STEPS:
        name, success, output = run_script(name, script)
        if not success:
            print(f"  [FAIL] {name}: {output[:300]}")
            sys.exit(1)
        print(f"  [OK]   {name}")

    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
