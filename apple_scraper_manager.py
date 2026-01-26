#!/usr/bin/env python3
"""
Apple Product Line Scraper Manager
Unified tool to scrape and compare prices across all Apple product lines
"""

import subprocess
import sys
import time
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

class AppleScraperManager:
    """Manage all Apple product line scrapers"""
    
    def __init__(self):
        self.product_lines = {
            'iphone': {
                'script': 'iphone.py',
                'output': 'iphone_products_merged.csv',
                'description': 'iPhone series (all models)',
                'priority': 1,
                'estimated_time': '5-10 minutes'
            },
            'ipad': {
                'script': 'ipad.py', 
                'output': 'ipad_products_merged.csv',
                'description': 'iPad series (Air, Pro, mini)',
                'priority': 2,
                'estimated_time': '3-8 minutes'
            },
            'mac': {
                'script': 'mac.py',
                'output': 'mac_products_merged.csv', 
                'description': 'Mac series (MacBook, iMac, Mac Pro)',
                'priority': 3,
                'estimated_time': '8-15 minutes'
            },
            'watch': {
                'script': 'watch.py',
                'output': 'watch_products_merged.csv',
                'description': 'Apple Watch series',
                'priority': 4,
                'estimated_time': '2-5 minutes'
            },
            'airpods': {
                'script': 'airpods.py',
                'output': 'airpods_products_merged.csv', 
                'description': 'AirPods series',
                'priority': 5,
                'estimated_time': '1-3 minutes'
            }
        }
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        try:
            import pandas as pd
            import requests
            from bs4 import BeautifulSoup
            print("✅ Core dependencies available")
            
            # Optional dependencies for plotting (not required for core functionality)
            optional_deps = []
            try:
                import matplotlib.pyplot as plt
                import seaborn as sns
                optional_deps.append("plotting")
            except ImportError:
                pass
            
            if optional_deps:
                print(f"✅ Optional dependencies: {', '.join(optional_deps)}")
            
            return True
        except ImportError as e:
            print(f"❌ Missing required dependency: {e}")
            print("❌ Please install: pip install requests beautifulsoup4 pandas")
            return False
    
    def run_single_scraper(self, product_line, timeout_minutes=30):
        """Run a single product line scraper"""
        config = self.product_lines[product_line]
        script_path = Path(config['script'])
        
        if not script_path.exists():
            return {
                'product_line': product_line,
                'status': 'error',
                'message': f"Script {config['script']} not found"
            }
        
        print(f"🚀 Starting {product_line} scraper...")
        print(f"   Estimated time: {config['estimated_time']}")
        
        try:
            # Run with timeout
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout_minutes * 60,
                cwd=Path.cwd()
            )
            
            if result.returncode == 0:
                # Check if output file was created
                output_path = Path(config['output'])
                if output_path.exists():
                    return {
                        'product_line': product_line,
                        'status': 'success',
                        'output_file': str(output_path),
                        'message': f"Successfully scraped {product_line}"
                    }
                else:
                    return {
                        'product_line': product_line, 
                        'status': 'warning',
                        'message': f"{product_line} script completed but no output file found"
                    }
            else:
                return {
                    'product_line': product_line,
                    'status': 'error', 
                    'message': f"{product_line} script failed",
                    'error': result.stderr[-500:] if result.stderr else "Unknown error"
                }
                
        except subprocess.TimeoutExpired:
            return {
                'product_line': product_line,
                'status': 'timeout',
                'message': f"{product_line} scraper timed out after {timeout_minutes} minutes"
            }
        except Exception as e:
            return {
                'product_line': product_line,
                'status': 'error',
                'message': f"Unexpected error running {product_line}: {str(e)}"
            }
    
    def run_all_scrapers(self, parallel=False, timeout_minutes=30):
        """Run all available scrapers"""
        if not self.check_dependencies():
            print("❌ Please install missing dependencies first")
            return {}
        
        results = {}
        
        if parallel:
            print("🔄 Running all scrapers in parallel...")
            with ThreadPoolExecutor(max_workers=3) as executor:
                # Submit all tasks
                future_to_product = {
                    executor.submit(self.run_single_scraper, product_line, timeout_minutes): product_line
                    for product_line in self.product_lines.keys()
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_product):
                    product_line = future_to_product[future]
                    try:
                        result = future.result()
                        results[product_line] = result
                        self._print_result(result)
                    except Exception as exc:
                        results[product_line] = {
                            'product_line': product_line,
                            'status': 'error',
                            'message': f'Generated an exception: {exc}'
                        }
        else:
            print("🔄 Running scrapers sequentially...")
            # Sort by priority
            sorted_products = sorted(
                self.product_lines.items(),
                key=lambda x: x[1]['priority']
            )
            
            for product_line, config in sorted_products:
                result = self.run_single_scraper(product_line, timeout_minutes)
                results[product_line] = result
                self._print_result(result)
        
        return results
    
    def _print_result(self, result):
        """Print result with appropriate emoji"""
        status = result['status']
        product_line = result['product_line']
        message = result.get('message', '')
        
        if status == 'success':
            print(f"✅ {product_line.title()}: {message}")
        elif status == 'warning':
            print(f"⚠️ {product_line.title()}: {message}")
        elif status == 'timeout':
            print(f"⏰ {product_line.title()}: {message}")
        else:
            print(f"❌ {product_line.title()}: {message}")
            if 'error' in result:
                print(f"   Error details: {result['error']}")
    
    def list_product_lines(self):
        """List all available product lines"""
        print("\n📱 Available Apple Product Lines:")
        print("=" * 50)
        
        for product_line, config in self.product_lines.items():
            status = "✅" if Path(config['script']).exists() else "❌"
            print(f"{status} {product_line.title()}: {config['description']}")
            print(f"   Script: {config['script']}")
            print(f"   Est. time: {config['estimated_time']}")
            print()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Apple Product Line Scraper Manager")
    parser.add_argument(
        'command',
        choices=['list', 'run-all', 'run'],
        help='Command to execute'
    )
    parser.add_argument(
        '--product',
        choices=['iphone', 'ipad', 'mac', 'watch', 'airpods'],
        help='Specific product line to run (for run command)'
    )
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run scrapers in parallel (faster but uses more resources)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Timeout per scraper in minutes (default: 30)'
    )
    
    args = parser.parse_args()
    manager = AppleScraperManager()
    
    if args.command == 'list':
        manager.list_product_lines()
    
    elif args.command == 'run-all':
        print("🍎 Apple Product Line Price Comparison Tool")
        print("=" * 50)
        results = manager.run_all_scrapers(parallel=args.parallel, timeout_minutes=args.timeout)
        
        # Summary
        successful = sum(1 for r in results.values() if r['status'] == 'success')
        total = len(results)
        print(f"\n📊 Summary: {successful}/{total} scrapers completed successfully")
        
    elif args.command == 'run':
        if not args.product:
            print("❌ Please specify --product for single run")
            sys.exit(1)
            
        result = manager.run_single_scraper(args.product, timeout_minutes=args.timeout)
        manager._print_result(result)

if __name__ == '__main__':
    main()