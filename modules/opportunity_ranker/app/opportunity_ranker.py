#!/usr/bin/env python3
"""
Opportunity Ranker Module
Aggregates and prioritizes trading opportunities from multiple sources.

Usage:
    python -m modules.opportunity_ranker.app.opportunity_ranker [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/ranker"))

# --- Weights for Final Score ---
WEIGHTS = {
    "scanner": 0.3,
    "probability": 0.5,
    "liquidation": 0.2
}

# --- Core Logic ---
class OpportunityRanker:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def load_input(self, input_path):
        """Load and parse input JSON."""
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
                # If single object, wrap in list? No, expect lists from modules.
                print(f"Error: Input JSON must be a list of objects ({input_path}).")
                sys.exit(1)
            return data

    def merge_data(self, scanner_data, liq_data, prob_data):
        """Merge data sources by symbol."""
        merged = {}
        
        # Helper to merge dicts
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(scanner_data, "scanner")
        merge_list(liq_data, "liquidation")
        merge_list(prob_data, "probability")
        
        return merged

    def calculate_opportunity_score(self, data):
        """Calculate unified score (0.0 to 1.0)."""
        # Scanner: scan_score (-1 to 1) -> Normalize to 0-1? Or keep directional?
        # Let's target an absolute "Strength" score (0-1) and a "Bias" (Long/Short).
        
        # Scanner Score (-1 to 1)
        scan = data.get("scanner", {}).get("scan_score", 0.0)
        
        # Probability (Long 0-1, Short 0-1)
        # Convert to directional score: ProbLong - ProbShort (-1 to 1)
        prob_obj = data.get("probability", {})
        p_long = prob_obj.get("probability_long", 0.5)
        p_short = prob_obj.get("probability_short", 0.5)
        prob_score = p_long - p_short
        
        # Liquidation Score (-1 to 1)
        # Remember: Liq < 0 (Longs Wiped) -> Bearish? Or Reversal Bullish?
        # In `LiquidationAnalyzer`:
        #   Negative Score = Longs Wiped (Bearish Pressure)
        #   Positive Score = Shorts Wiped (Bullish Pressure)
        # So it aligns with -1 (Bearish) to 1 (Bullish).
        liq = data.get("liquidation", {}).get("liquidation_score", 0.0)
        
        # Weighted Average of Directional Scores
        final_dir_score = (
            scan * WEIGHTS["scanner"] +
            prob_score * WEIGHTS["probability"] +
            liq * WEIGHTS["liquidation"]
        )
        
        # Opportunity Score = Magnitude (0 to 1)
        opportunity_score = abs(final_dir_score)
        
        # Bias
        bias = "NEUTRAL"
        if final_dir_score > 0.1: bias = "LONG"
        elif final_dir_score < -0.1: bias = "SHORT"
        
        # Confidence logic (simple average of input confidences/strengths)
        # Scanner strength: abs(scan)
        # Prob confidence: prob_obj.get("confidence", 0)
        # Liq intensity: abs(liq)
        confidence = (abs(scan) + prob_obj.get("confidence", 0.5) + abs(liq)) / 3.0
        
        return round(opportunity_score, 2), bias, round(confidence, 2)

    def rank_opportunities(self, merged_data):
        ranked = []
        for sym, data in merged_data.items():
            score, bias, conf = self.calculate_opportunity_score(data)
            
            # Filter weak signals? No, list all but prioritize.
            priority = "LOW"
            if score > 0.7: priority = "HIGH"
            elif score > 0.4: priority = "MEDIUM"
            
            # Generate Summary
            drivers = []
            if "scanner" in data: drivers.append("Scanner")
            if "probability" in data: drivers.append("Probability")
            if "liquidation" in data: drivers.append("Liquidation")
            
            summary = f"{priority} priority {bias} setup (Score: {score}). Supported by {', '.join(drivers)}."
            
            ranked.append({
                "symbol": sym,
                "opportunity_score": score,
                "priority": priority,
                "setup_bias": bias,
                "confidence": conf,
                "summary": summary,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "_details": {
                    "scan_score": data.get("scanner", {}).get("scan_score", 0),
                    "prob_long": data.get("probability", {}).get("probability_long", 0),
                    "liq_score": data.get("liquidation", {}).get("liquidation_score", 0)
                }
            })
            
        # Sort by score descending
        ranked.sort(key=lambda x: x["opportunity_score"], reverse=True)
        
        # Assign Rank
        for i, item in enumerate(ranked):
            item["rank"] = i + 1
            
        return ranked

    def run_rank(self, scanner_path, liq_path, prob_path):
        s_data = self.load_input(scanner_path)
        l_data = self.load_input(liq_path)
        p_data = self.load_input(prob_path)
        
        merged = self.merge_data(s_data, l_data, p_data)
        ranked = self.rank_opportunities(merged)
        
        print(json.dumps(ranked, indent=2))
        return ranked

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_rank(
            CONFIG_DIR / "sample_scanner.json",
            CONFIG_DIR / "sample_liquidations.json",
            CONFIG_DIR / "sample_probability.json"
        )

    def export_results(self, ranked_data=None, output_path=None):
        if not ranked_data:
            ranked_data = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"ranked_opportunities_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(ranked_data, f, indent=2)
        print(f"Exported ranked opportunities to: {output_path}")

    def explain_results(self, scanner_path, liq_path, prob_path):
        ranked = self.run_rank(scanner_path, liq_path, prob_path)
        print("\n=== Opportunity Ranker Explanation ===\n")
        print(f"Weights: {json.dumps(WEIGHTS, indent=2)}")
        print("Logic: Weighted average of directional scores (-1 to 1).")
        print("       Final Score = Magnitude (0 to 1). Bias = Direction.\n")
        
        for item in ranked:
            print(f"#{item['rank']} {item['symbol']} ({item['priority']})")
            print(f"  Score: {item['opportunity_score']} | Bias: {item['setup_bias']} | Conf: {item['confidence']}")
            print(f"  Summary: {item['summary']}")
            det = item["_details"]
            print(f"  Inputs: Scan={det['scan_score']}, ProbLong={det['prob_long']}, Liq={det['liq_score']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Opportunity Ranker")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    rank_parser = subparsers.add_parser("rank", help="Rank inputs")
    rank_parser.add_argument("--scanner", required=True, help="Scanner results JSON")
    rank_parser.add_argument("--liquidations", required=True, help="Liquidation results JSON")
    rank_parser.add_argument("--probability", required=True, help="Probability results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain ranking logic")
    explain_parser.add_argument("--scanner", help="Scanner results JSON")
    explain_parser.add_argument("--liquidations", help="Liquidation results JSON")
    explain_parser.add_argument("--probability", help="Probability results JSON")

    args = parser.parse_args()
    ranker = OpportunityRanker()

    if args.command == "status":
        print("Opportunity Ranker Status: OK")
        print(f"Output Dir: {ranker.output_dir}")
        print(f"Weights: {json.dumps(WEIGHTS)}")
    elif args.command == "sample":
        ranker.run_sample()
    elif args.command == "rank":
        ranker.run_rank(args.scanner, args.liquidations, args.probability)
    elif args.command == "export":
        ranker.export_results(output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        scanner = args.scanner if args.scanner else CONFIG_DIR / "sample_scanner.json"
        liq = args.liquidations if args.liquidations else CONFIG_DIR / "sample_liquidations.json"
        prob = args.probability if args.probability else CONFIG_DIR / "sample_probability.json"
        ranker.explain_results(scanner, liq, prob)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
