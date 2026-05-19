#!/usr/bin/env python3
"""
Liquidation Analyzer Module
Analyzes liquidation data to determine market bias.

Usage:
    python -m modules.liquidation_analyzer.app.liquidation_analyzer [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/liquidation"))

# --- Core Logic ---
class LiquidationAnalyzer:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def load_input(self, input_path):
        """Load and parse input JSON (list of liquidations)."""
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

    def calculate_metrics(self, asset):
        """Compute metrics for a single asset."""
        longs = float(asset.get("liquidations_long", 0))
        shorts = float(asset.get("liquidations_short", 0))
        oi = float(asset.get("open_interest", 1)) # avoid div/0
        
        total_liq = longs + shorts
        if total_liq == 0:
            return 0.0, 0.0, "BALANCED"

        # Ratio: -1.0 (All Longs) to +1.0 (All Shorts)
        # Standard convention: High Long Liqs -> Bearish flush (or bullish reversal if capitulation?)
        # Let's define "Score" as directional bias for Probability Engine:
        # If Longs are wiped -> Short term bearish pressure (selling) OR Reversal imminent?
        # Usually: Heavy Long Liquidations = Forced Selling = Price Down.
        # So Score < 0 (Bearish).
        # Heavy Short Liquidations = Forced Buying = Price Up.
        # So Score > 0 (Bullish).
        
        net_flow = shorts - longs # Positive if Shorts > Longs (Buying pressure), Negative if Longs > Shorts (Selling pressure)
        score = net_flow / total_liq # Normalized -1 to 1
        
        # Intensity: Liq / OI
        intensity_val = total_liq / oi if oi > 0 else 0
        
        return score, intensity_val, total_liq

    def analyze_asset(self, asset):
        """Analyze a single asset entry."""
        score, intensity_val, total_liq = self.calculate_metrics(asset)
        
        # Classification
        bias = "BALANCED"
        dominant_side = "NEUTRAL"
        
        if score < -0.2:
            bias = "LONGS_WIPED"
            dominant_side = "LONG"
        elif score > 0.2:
            bias = "SHORTS_WIPED"
            dominant_side = "SHORT"
            
        intensity = "LOW"
        if intensity_val > 0.05: # >5% of OI wiped is huge
            intensity = "HIGH"
        elif intensity_val > 0.01:
            intensity = "MEDIUM"
            
        # Summary
        summary = f"{bias} ({dominant_side} dominant)."
        if intensity == "HIGH":
            summary = f"Heavy {dominant_side.lower()} liquidations detected ({intensity})."
        elif intensity == "MEDIUM":
            summary = f"Moderate {dominant_side.lower()} liquidations."
            
        return {
            "symbol": asset.get("symbol", "UNKNOWN"),
            "timestamp": asset.get("timestamp", datetime.now(timezone.utc).isoformat()),
            "liquidation_bias": bias,
            "liquidation_score": round(score, 2),
            "intensity": intensity,
            "dominant_side": dominant_side,
            "summary": summary,
            "raw_metrics": {
                "longs": asset.get("liquidations_long", 0),
                "shorts": asset.get("liquidations_short", 0),
                "ratio_val": round(intensity_val, 4)
            }
        }

    def analyze(self, assets):
        """Process a list of assets."""
        results = []
        for asset in assets:
            res = self.analyze_asset(asset)
            results.append(res)
        
        # Sort by intensity? Or just return list.
        # Let's sort by absolute score (imbalance)
        results.sort(key=lambda x: abs(x["liquidation_score"]), reverse=True)
        return results

    def run_sample(self):
        """Run with internal sample data."""
        sample_path = CONFIG_DIR / "sample_liquidations.json"
        if sample_path.exists():
            assets = self.load_input(sample_path)
        else:
            assets = [{
                "symbol": "MOCK", 
                "liquidations_long": 1000, 
                "liquidations_short": 100, 
                "open_interest": 10000
            }]
        
        results = self.analyze(assets)
        print(json.dumps(results, indent=2))
        return results

    def run_analyze(self, input_path):
        assets = self.load_input(input_path)
        results = self.analyze(assets)
        print(json.dumps(results, indent=2))
        return results

    def export_results(self, input_path=None, output_path=None):
        assets = self.load_input(input_path) if input_path else self.load_input(CONFIG_DIR / "sample_liquidations.json")
        results = self.analyze(assets)
        
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"liquidation_results_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Exported liquidation results to: {output_path}")

    def explain_results(self, input_path):
        assets = self.load_input(input_path)
        results = self.analyze(assets)
        
        print("\n=== Liquidation Analysis Explanation ===\n")
        print("Logic: Score = (Shorts - Longs) / Total. Range [-1, 1].")
        print("       Negative Score -> Longs Wiped (Bearish Pressure).")
        print("       Positive Score -> Shorts Wiped (Bullish Pressure).")
        print("       Intensity = Total Liq / Open Interest.\n")
        
        for res in results:
            print(f"Symbol: {res['symbol']}")
            print(f"  Bias: {res['liquidation_bias']}")
            print(f"  Score: {res['liquidation_score']}")
            print(f"  Intensity: {res['intensity']}")
            print(f"  Summary: {res['summary']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Liquidation Analyzer")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    analyze_parser = subparsers.add_parser("analyze", help="Analyze input liquidations")
    analyze_parser.add_argument("--input", help="Path to input JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--input", help="Path to input JSON")
    exp_parser.add_argument("--output", help="Path to output file")

    explain_parser = subparsers.add_parser("explain", help="Explain analysis logic")
    explain_parser.add_argument("--input", required=True, help="Path to input JSON")

    args = parser.parse_args()
    analyzer = LiquidationAnalyzer()

    if args.command == "status":
        print("Liquidation Analyzer Status: OK")
        print(f"Output Dir: {analyzer.output_dir}")
    elif args.command == "sample":
        analyzer.run_sample()
    elif args.command == "analyze":
        if args.input:
            analyzer.run_analyze(args.input)
        else:
            analyzer.run_sample()
    elif args.command == "export":
        analyzer.export_results(args.input, args.output)
    elif args.command == "explain":
        analyzer.explain_results(args.input)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
