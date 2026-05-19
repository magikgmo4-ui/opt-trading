#!/usr/bin/env python3
"""
Market Scanner Module
Identifies trading opportunities based on market data scores.

Usage:
    python -m modules.market_scanner.app.market_scanner [command] [args]
"""
import sys
import os
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ---
MODULE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MODULE_DIR.parent.parent
CONFIG_DIR = MODULE_DIR / "config"

def get_output_dir(path_str):
    """Resolve output directory relative to project root if not absolute."""
    p = Path(path_str)
    if p.is_absolute():
        return p
    return PROJECT_ROOT / p

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/scan"))

# --- Scoring Weights ---
WEIGHTS = {
    "trend_score": 0.4,
    "momentum_score": 0.2,
    "volatility_score": 0.1,
    "liquidity_score": 0.2,
    "open_interest_score": 0.1
}

# --- Core Logic ---
class MarketScanner:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def load_input(self, input_path):
        """Load and parse input JSON (list of assets)."""
        p = Path(input_path)
        if not p.exists():
            # Try relative to project root
            p = PROJECT_ROOT / input_path
            if not p.exists():
                print(f"Error: Input file not found: {input_path}")
                sys.exit(1)
        
        with open(p, "r") as f:
            data = json.load(f)
            if not isinstance(data, list):
                print("Error: Input JSON must be a list of asset objects.")
                sys.exit(1)
            return data

    def calculate_scan_score(self, asset):
        """Calculate weighted score for a single asset."""
        total_score = 0.0
        total_weight = 0.0
        
        for key, weight in WEIGHTS.items():
            val = asset.get(key, 0.0)
            # Clamp value between -1.0 and 1.0 (assuming input is normalized, but safe check)
            val = max(-1.0, min(1.0, float(val)))
            total_score += val * weight
            total_weight += weight
            
        return total_score / total_weight if total_weight > 0 else 0.0

    def classify_opportunity(self, score, asset):
        """Determine bias, priority, and summary based on score."""
        bias = "NEUTRAL"
        priority = "LOW"
        
        if score > 0.2:
            bias = "LONG"
        elif score < -0.2:
            bias = "SHORT"
            
        abs_score = abs(score)
        if abs_score > 0.6:
            priority = "HIGH"
        elif abs_score > 0.3:
            priority = "MEDIUM"
            
        # Simple summary generation
        drivers = []
        if abs(asset.get("trend_score", 0)) > 0.5: drivers.append("Trend")
        if abs(asset.get("momentum_score", 0)) > 0.5: drivers.append("Momentum")
        if asset.get("liquidity_score", 0) > 0.7: drivers.append("Liquidity")
        
        summary = f"{priority} {bias} signal."
        if drivers:
            summary += f" Driven by {', '.join(drivers)}."
            
        return bias, priority, summary

    def scan(self, assets):
        """Process a list of assets and return ranked opportunities."""
        results = []
        for asset in assets:
            score = self.calculate_scan_score(asset)
            bias, priority, summary = self.classify_opportunity(score, asset)
            
            result = {
                "symbol": asset.get("symbol", "UNKNOWN"),
                "scan_score": round(score, 3),
                "setup_bias": bias,
                "priority": priority,
                "summary": summary,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            results.append(result)
            
        # Sort by absolute score descending (strongest signals first)
        results.sort(key=lambda x: abs(x["scan_score"]), reverse=True)
        return results

    def run_sample(self):
        """Run with internal sample data."""
        sample_path = CONFIG_DIR / "sample_markets.json"
        if sample_path.exists():
            assets = self.load_input(sample_path)
        else:
            # Fallback mock
            assets = [{"symbol": "MOCK", "trend_score": 0.8}]
            
        results = self.scan(assets)
        print(json.dumps(results, indent=2))
        return results

    def run_scan(self, input_path):
        assets = self.load_input(input_path)
        results = self.scan(assets)
        print(json.dumps(results, indent=2))
        return results

    def export_results(self, input_path=None, output_path=None):
        assets = self.load_input(input_path) if input_path else self.load_input(CONFIG_DIR / "sample_markets.json")
        results = self.scan(assets)
        
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"scan_results_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Exported scan results to: {output_path}")

    def explain_results(self, input_path):
        assets = self.load_input(input_path)
        results = self.scan(assets)
        
        print("\n=== Market Scan Explanation ===\n")
        print(f"Weights Used: {json.dumps(WEIGHTS, indent=2)}\n")
        
        for res in results:
            print(f"Symbol: {res['symbol']}")
            print(f"  Score: {res['scan_score']}")
            print(f"  Bias: {res['setup_bias']}")
            print(f"  Priority: {res['priority']}")
            print(f"  Summary: {res['summary']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Market Scanner")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    scan_parser = subparsers.add_parser("scan", help="Scan input markets")
    scan_parser.add_argument("--input", help="Path to input JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export scan results")
    exp_parser.add_argument("--input", help="Path to input JSON")
    exp_parser.add_argument("--output", help="Path to output file")

    explain_parser = subparsers.add_parser("explain", help="Explain scan results")
    explain_parser.add_argument("--input", required=True, help="Path to input JSON")

    args = parser.parse_args()
    scanner = MarketScanner()

    if args.command == "status":
        print("Market Scanner Status: OK")
        print(f"Output Dir: {scanner.output_dir}")
        print(f"Active Weights: {list(WEIGHTS.keys())}")
    elif args.command == "sample":
        scanner.run_sample()
    elif args.command == "scan":
        if args.input:
            scanner.run_scan(args.input)
        else:
            scanner.run_sample()
    elif args.command == "export":
        scanner.export_results(args.input, args.output)
    elif args.command == "explain":
        scanner.explain_results(args.input)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
