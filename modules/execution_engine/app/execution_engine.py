#!/usr/bin/env python3
"""
Execution Engine Module
Translates risk-approved decisions into execution plans (Paper Mode).

Usage:
    python -m modules.execution_engine.app.execution_engine [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/execution"))

# --- Core Logic ---
class ExecutionEngine:
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

    def merge_data(self, decisions, risk):
        """Merge data sources by symbol."""
        merged = {}
        
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(decisions, "decision")
        merge_list(risk, "risk")
        
        return merged

    def plan_symbol(self, symbol, data):
        """Generate execution plan for a single symbol."""
        
        dec = data.get("decision", {})
        rsk = data.get("risk", {})
        
        decision_val = dec.get("decision", "WAIT")
        risk_status = rsk.get("risk_status", "BLOCK")
        allowed_action = rsk.get("allowed_action", "NO_TRADE")
        max_risk_pct = rsk.get("max_risk_pct", 0.0)
        sizing_hint = rsk.get("sizing_hint", "NONE")
        
        execution_status = "BLOCKED"
        execution_mode = "PAPER"
        action = "NO_ACTION"
        routing_hint = "blocked"
        rationale = []
        
        # 1. Check Risk Approval
        if risk_status == "BLOCK":
            execution_status = "BLOCKED"
            action = "NO_ACTION"
            rationale.append("Blocked by Risk Engine.")
            
        elif risk_status in ["ALLOW", "CAUTION"]:
            # 2. Match Decision to Allowed Action
            if decision_val == "GO_LONG":
                if allowed_action in ["LONG_ONLY", "ANY"]:
                    execution_status = "READY"
                    action = "PREPARE_LONG"
                    routing_hint = "paper-long"
                    rationale.append(f"Approved LONG ({sizing_hint} size).")
                else:
                    execution_status = "BLOCKED"
                    rationale.append(f"Decision GO_LONG but allowed action is {allowed_action}.")
                    
            elif decision_val == "GO_SHORT":
                if allowed_action in ["SHORT_ONLY", "ANY"]:
                    execution_status = "READY"
                    action = "PREPARE_SHORT"
                    routing_hint = "paper-short"
                    rationale.append(f"Approved SHORT ({sizing_hint} size).")
                else:
                    execution_status = "BLOCKED"
                    rationale.append(f"Decision GO_SHORT but allowed action is {allowed_action}.")
            
            else:
                execution_status = "HOLD"
                action = "HOLD"
                rationale.append(f"Decision is {decision_val}, no execution needed.")
        
        else:
             execution_status = "BLOCKED"
             rationale.append(f"Unknown risk status: {risk_status}")

        return {
            "symbol": symbol,
            "execution_status": execution_status,
            "execution_mode": execution_mode,
            "action": action,
            "size_hint": sizing_hint,
            "max_risk_pct": max_risk_pct,
            "routing_hint": routing_hint,
            "rationale": "; ".join(rationale),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def generate_plans(self, merged_data):
        plans = []
        for sym, data in merged_data.items():
            res = self.plan_symbol(sym, data)
            plans.append(res)
            
        # Sort: READY first, then HOLD, then BLOCKED
        status_map = {"READY": 3, "HOLD": 2, "BLOCKED": 1}
        plans.sort(key=lambda x: status_map.get(x["execution_status"], 0), reverse=True)
        return plans

    def run_plan(self, decisions_path, risk_path):
        d_data = self.load_input(decisions_path)
        r_data = self.load_input(risk_path)
        
        merged = self.merge_data(d_data, r_data)
        plans = self.generate_plans(merged)
        
        print(json.dumps(plans, indent=2))
        return plans

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_plan(
            CONFIG_DIR / "sample_decisions.json",
            CONFIG_DIR / "sample_risk.json"
        )

    def export_results(self, plans=None, output_path=None):
        if not plans:
            plans = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"execution_plans_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(plans, f, indent=2)
        print(f"Exported execution plans to: {output_path}")

    def explain_results(self, decisions_path, risk_path):
        plans = self.run_plan(decisions_path, risk_path)
        print("\n=== Execution Engine Explanation ===\n")
        print("Mode: PAPER ONLY (Simulation)\n")
        
        for item in plans:
            print(f"Symbol: {item['symbol']}")
            print(f"  Status: {item['execution_status']} -> {item['action']}")
            print(f"  Routing: {item['routing_hint']} (Size: {item['size_hint']})")
            print(f"  Rationale: {item['rationale']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Execution Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    plan_parser = subparsers.add_parser("plan", help="Generate execution plans")
    plan_parser.add_argument("--decisions", help="Decision results JSON")
    plan_parser.add_argument("--risk", help="Risk results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--decisions", help="Decision results JSON")
    exp_parser.add_argument("--risk", help="Risk results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain execution logic")
    explain_parser.add_argument("--decisions", help="Decision results JSON")
    explain_parser.add_argument("--risk", help="Risk results JSON")

    args = parser.parse_args()
    engine = ExecutionEngine()

    if args.command == "status":
        print("Execution Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
        print("Mode: PAPER ONLY")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "plan":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        engine.run_plan(dec, risk)
    elif args.command == "export":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        plans = engine.run_plan(dec, risk)
        engine.export_results(plans, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        engine.explain_results(dec, risk)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
