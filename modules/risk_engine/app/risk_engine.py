#!/usr/bin/env python3
"""
Risk Engine Module
Evaluates and sizes trades based on risk parameters.

Usage:
    python -m modules.risk_engine.app.risk_engine [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/risk"))

# --- Risk Parameters ---
RISK_PARAMS = {
    "min_confidence_allow": 0.6,
    "high_confidence_threshold": 0.8,
    "min_rank_priority_full": "HIGH",
    "base_risk_pct": 1.0, # 1% account risk
}

# --- Core Logic ---
class RiskEngine:
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

    def merge_data(self, decisions, ranker, probability):
        """Merge data sources by symbol."""
        merged = {}
        
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(decisions, "decision")
        merge_list(ranker, "ranker")
        merge_list(probability, "probability")
        
        return merged

    def assess_symbol(self, symbol, data):
        """Apply risk rules to a single symbol."""
        
        dec = data.get("decision", {})
        rank = data.get("ranker", {})
        prob = data.get("probability", {})
        
        decision_val = dec.get("decision", "WAIT")
        confidence = dec.get("confidence", 0.0)
        review_prio = dec.get("review_priority", "LOW")
        
        rank_prio = rank.get("priority", "LOW")
        
        prob_long = prob.get("probability_long", 0.5)
        prob_short = prob.get("probability_short", 0.5)
        
        # Defaults
        risk_status = "BLOCK"
        risk_tier = "HIGH"
        max_risk_pct = 0.0
        sizing_hint = "NONE"
        allowed_action = "NO_TRADE"
        invalidation_hint = "N/A"
        rationale = []
        
        # Logic
        if decision_val in ["WAIT", "REJECT"]:
            risk_status = "BLOCK"
            allowed_action = "NO_TRADE"
            rationale.append(f"Decision is {decision_val}.")
            invalidation_hint = "Wait for clearer signal."
            
        elif decision_val in ["GO_LONG", "GO_SHORT"]:
            direction = "LONG" if decision_val == "GO_LONG" else "SHORT"
            
            # 1. Confidence Check
            if confidence < RISK_PARAMS["min_confidence_allow"]:
                risk_status = "BLOCK"
                rationale.append(f"Confidence {confidence} too low (< {RISK_PARAMS['min_confidence_allow']}).")
                invalidation_hint = "Confidence needs to improve."
            else:
                risk_status = "ALLOW"
                allowed_action = f"{direction}_ONLY"
                
                # 2. Sizing / Tiering
                # FULL size criteria: High Rank Priority AND High Confidence
                if rank_prio == "HIGH" and confidence >= RISK_PARAMS["high_confidence_threshold"]:
                    risk_tier = "LOW" # Low risk setup = Good
                    max_risk_pct = RISK_PARAMS["base_risk_pct"]
                    sizing_hint = "FULL"
                    rationale.append("High quality setup (High Rank & Conf).")
                elif rank_prio == "MEDIUM" or confidence >= RISK_PARAMS["min_confidence_allow"]:
                    risk_tier = "MEDIUM"
                    max_risk_pct = RISK_PARAMS["base_risk_pct"] * 0.5
                    sizing_hint = "HALF"
                    rationale.append("Medium quality setup.")
                else:
                    risk_tier = "HIGH"
                    max_risk_pct = RISK_PARAMS["base_risk_pct"] * 0.25
                    sizing_hint = "MICRO"
                    rationale.append("Low quality but allowed setup.")
                    
                # Invalidation
                invalidation_hint = f"Invalidate if {direction.lower()} structure breaks or confidence drops."
                
        # Review Priority Override
        if review_prio == "HIGH" and risk_status == "ALLOW":
            risk_status = "CAUTION"
            rationale.append("Decision flagged for High Review Priority.")
            if sizing_hint == "FULL":
                sizing_hint = "HALF"
                max_risk_pct *= 0.5

        return {
            "symbol": symbol,
            "risk_status": risk_status,
            "risk_tier": risk_tier,
            "max_risk_pct": round(max_risk_pct, 2),
            "sizing_hint": sizing_hint,
            "allowed_action": allowed_action,
            "invalidation_hint": invalidation_hint,
            "rationale": "; ".join(rationale),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def assess_risk(self, merged_data):
        assessments = []
        for sym, data in merged_data.items():
            res = self.assess_symbol(sym, data)
            assessments.append(res)
            
        # Sort: ALLOW first, then sizing hint
        size_map = {"FULL": 4, "HALF": 3, "MICRO": 2, "NONE": 1}
        assessments.sort(key=lambda x: (x["risk_status"] == "ALLOW", size_map.get(x["sizing_hint"], 0)), reverse=True)
        return assessments

    def run_assess(self, decisions_path, ranker_path, prob_path):
        d_data = self.load_input(decisions_path)
        r_data = self.load_input(ranker_path)
        p_data = self.load_input(prob_path)
        
        merged = self.merge_data(d_data, r_data, p_data)
        assessments = self.assess_risk(merged)
        
        print(json.dumps(assessments, indent=2))
        return assessments

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_assess(
            CONFIG_DIR / "sample_decisions.json",
            CONFIG_DIR / "sample_ranker.json",
            CONFIG_DIR / "sample_probability.json"
        )

    def export_results(self, assessments=None, output_path=None):
        if not assessments:
            assessments = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"risk_assessments_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(assessments, f, indent=2)
        print(f"Exported risk assessments to: {output_path}")

    def explain_results(self, decisions_path, ranker_path, prob_path):
        assessments = self.run_assess(decisions_path, ranker_path, prob_path)
        print("\n=== Risk Engine Explanation ===\n")
        print(f"Params: {json.dumps(RISK_PARAMS, indent=2)}\n")
        
        for item in assessments:
            print(f"Symbol: {item['symbol']}")
            print(f"  Status: {item['risk_status']} ({item['allowed_action']})")
            print(f"  Sizing: {item['sizing_hint']} ({item['max_risk_pct']}%)")
            print(f"  Rationale: {item['rationale']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Risk Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    assess_parser = subparsers.add_parser("assess", help="Assess risk")
    assess_parser.add_argument("--decisions", help="Decision results JSON")
    assess_parser.add_argument("--ranker", help="Ranker results JSON")
    assess_parser.add_argument("--probability", help="Probability results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--decisions", help="Decision results JSON")
    exp_parser.add_argument("--ranker", help="Ranker results JSON")
    exp_parser.add_argument("--probability", help="Probability results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain risk logic")
    explain_parser.add_argument("--decisions", help="Decision results JSON")
    explain_parser.add_argument("--ranker", help="Ranker results JSON")
    explain_parser.add_argument("--probability", help="Probability results JSON")

    args = parser.parse_args()
    engine = RiskEngine()

    if args.command == "status":
        print("Risk Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
        print(f"Params: {json.dumps(RISK_PARAMS)}")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "assess":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        rank = args.ranker if args.ranker else CONFIG_DIR / "sample_ranker.json"
        prob = args.probability if args.probability else CONFIG_DIR / "sample_probability.json"
        engine.run_assess(dec, rank, prob)
    elif args.command == "export":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        rank = args.ranker if args.ranker else CONFIG_DIR / "sample_ranker.json"
        prob = args.probability if args.probability else CONFIG_DIR / "sample_probability.json"
        assessments = engine.run_assess(dec, rank, prob)
        engine.export_results(assessments, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        rank = args.ranker if args.ranker else CONFIG_DIR / "sample_ranker.json"
        prob = args.probability if args.probability else CONFIG_DIR / "sample_probability.json"
        engine.explain_results(dec, rank, prob)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
