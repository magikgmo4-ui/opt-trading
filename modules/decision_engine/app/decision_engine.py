#!/usr/bin/env python3
"""
Decision Engine Module
Makes final trading decisions based on aggregated data.

Usage:
    python -m modules.decision_engine.app.decision_engine [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/decision"))

# --- Thresholds ---
THRESHOLDS = {
    "high_prob": 0.7,
    "min_prob": 0.6,
    "min_rank_score": 0.6,
    "high_confidence": 0.7
}

# --- Core Logic ---
class DecisionEngine:
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
                print(f"Error: Input JSON must be a list of objects ({input_path}).")
                sys.exit(1)
            return data

    def merge_data(self, ranker_data, prob_data, liq_data):
        """Merge data sources by symbol."""
        merged = {}
        
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(ranker_data, "ranker")
        merge_list(prob_data, "probability")
        merge_list(liq_data, "liquidation")
        
        return merged

    def evaluate_symbol(self, symbol, data):
        """Apply decision rules to a single symbol."""
        
        ranker = data.get("ranker", {})
        prob = data.get("probability", {})
        liq = data.get("liquidation", {})
        
        # Extract key metrics
        rank_score = ranker.get("opportunity_score", 0.0)
        setup_bias = ranker.get("setup_bias", "NEUTRAL")
        rank_priority = ranker.get("priority", "LOW")
        
        prob_long = prob.get("probability_long", 0.5)
        prob_short = prob.get("probability_short", 0.5)
        prob_conf = prob.get("confidence", 0.0)
        
        liq_bias = liq.get("liquidation_bias", "BALANCED")
        liq_intensity = liq.get("intensity", "LOW")
        
        decision = "WAIT"
        rationale = []
        review_priority = "LOW"
        
        # --- Rule Evaluation ---
        
        # 1. Reject weak ranker signals immediately
        if rank_score < 0.3:
            return {
                "symbol": symbol,
                "decision": "REJECT",
                "confidence": prob_conf,
                "decision_score": rank_score,
                "directional_bias": setup_bias,
                "review_priority": "LOW",
                "rationale": "Ranker score too low.",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        # 2. Check Directional Alignment
        if setup_bias == "LONG":
            # Probability Check
            if prob_long >= THRESHOLDS["min_prob"]:
                # Liquidation Check (Contradiction check)
                # If Longs were just wiped (Bearish flush?), usually implies short term bearish pressure OR capitulation bottom.
                # If Shorts were wiped (Bullish flush?), usually implies bullish squeeze.
                # Contradiction: Going Long when Shorts were just wiped heavily (might be top of squeeze).
                # Support: Going Long when Longs were wiped (capitulation) -> depends on strategy.
                # Let's assume standard trend following:
                # We want Prob to be high.
                
                decision = "GO_LONG"
                rationale.append(f"Ranker High ({rank_score})")
                rationale.append(f"Prob Long {prob_long}")
                
                if liq_bias == "SHORTS_WIPED" and liq_intensity == "HIGH":
                    rationale.append("Warning: Shorts just wiped (potential local top).")
                    review_priority = "HIGH" # Needs manual check
                
            else:
                decision = "WAIT"
                rationale.append(f"Prob Long {prob_long} below threshold {THRESHOLDS['min_prob']}")

        elif setup_bias == "SHORT":
            if prob_short >= THRESHOLDS["min_prob"]:
                decision = "GO_SHORT"
                rationale.append(f"Ranker High ({rank_score})")
                rationale.append(f"Prob Short {prob_short}")
                
                if liq_bias == "LONGS_WIPED" and liq_intensity == "HIGH":
                    rationale.append("Warning: Longs just wiped (potential local bottom).")
                    review_priority = "HIGH"
            else:
                decision = "WAIT"
                rationale.append(f"Prob Short {prob_short} below threshold {THRESHOLDS['min_prob']}")
        
        else:
            decision = "WAIT"
            rationale.append("Neutral setup bias.")

        # 3. Confidence Adjustment
        if decision.startswith("GO"):
            if prob_conf < 0.5:
                decision = "WAIT"
                rationale.append("Confidence too low.")
            elif prob_conf > THRESHOLDS["high_confidence"]:
                review_priority = "HIGH"
                rationale.append("High confidence setup.")
                
        # Final formatting
        return {
            "symbol": symbol,
            "decision": decision,
            "confidence": prob_conf,
            "decision_score": rank_score, # Using ranker score as proxy for now
            "directional_bias": setup_bias,
            "review_priority": review_priority,
            "rationale": "; ".join(rationale),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def make_decisions(self, merged_data):
        decisions = []
        for sym, data in merged_data.items():
            res = self.evaluate_symbol(sym, data)
            decisions.append(res)
            
        # Sort by review priority (HIGH first) then score
        priority_map = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        decisions.sort(key=lambda x: (priority_map.get(x.get("review_priority", "LOW"), 0), x.get("decision_score", 0)), reverse=True)
        return decisions

    def run_decide(self, ranker_path, prob_path, liq_path):
        r_data = self.load_input(ranker_path)
        p_data = self.load_input(prob_path)
        l_data = self.load_input(liq_path)
        
        merged = self.merge_data(r_data, p_data, l_data)
        decisions = self.make_decisions(merged)
        
        print(json.dumps(decisions, indent=2))
        return decisions

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_decide(
            CONFIG_DIR / "sample_ranker.json",
            CONFIG_DIR / "sample_probability.json",
            CONFIG_DIR / "sample_liquidations.json"
        )

    def export_results(self, decisions=None, output_path=None):
        if not decisions:
            decisions = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"decisions_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(decisions, f, indent=2)
        print(f"Exported decisions to: {output_path}")

    def explain_results(self, ranker_path, prob_path, liq_path):
        decisions = self.run_decide(ranker_path, prob_path, liq_path)
        print("\n=== Decision Engine Explanation ===\n")
        print(f"Thresholds: {json.dumps(THRESHOLDS, indent=2)}\n")
        
        for item in decisions:
            print(f"Symbol: {item['symbol']}")
            print(f"  Decision: {item['decision']} ({item['directional_bias']})")
            print(f"  Priority: {item['review_priority']}")
            print(f"  Rationale: {item['rationale']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Decision Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    decide_parser = subparsers.add_parser("decide", help="Make decisions")
    decide_parser.add_argument("--ranker", help="Ranker results JSON")
    decide_parser.add_argument("--probability", help="Probability results JSON")
    decide_parser.add_argument("--liquidations", help="Liquidation results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--ranker", help="Ranker results JSON")
    exp_parser.add_argument("--probability", help="Probability results JSON")
    exp_parser.add_argument("--liquidations", help="Liquidation results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain decision logic")
    explain_parser.add_argument("--ranker", help="Ranker results JSON")
    explain_parser.add_argument("--probability", help="Probability results JSON")
    explain_parser.add_argument("--liquidations", help="Liquidation results JSON")

    args = parser.parse_args()
    engine = DecisionEngine()

    if args.command == "status":
        print("Decision Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
        print(f"Thresholds: {json.dumps(THRESHOLDS)}")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "decide":
        # Use provided args or defaults
        ranker = args.ranker if args.ranker else CONFIG_DIR / "sample_ranker.json"
        prob = args.probability if args.probability else CONFIG_DIR / "sample_probability.json"
        liq = args.liquidations if args.liquidations else CONFIG_DIR / "sample_liquidations.json"
        engine.run_decide(ranker, prob, liq)
    elif args.command == "export":
        # Use provided args or defaults
        ranker = args.ranker if hasattr(args, 'ranker') and args.ranker else CONFIG_DIR / "sample_ranker.json"
        prob = args.probability if hasattr(args, 'probability') and args.probability else CONFIG_DIR / "sample_probability.json"
        liq = args.liquidations if hasattr(args, 'liquidations') and args.liquidations else CONFIG_DIR / "sample_liquidations.json"
        # We need to run decide first to get the data
        decisions = engine.run_decide(ranker, prob, liq)
        engine.export_results(decisions, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        ranker = args.ranker if args.ranker else CONFIG_DIR / "sample_ranker.json"
        prob = args.probability if args.probability else CONFIG_DIR / "sample_probability.json"
        liq = args.liquidations if args.liquidations else CONFIG_DIR / "sample_liquidations.json"
        engine.explain_results(ranker, prob, liq)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
