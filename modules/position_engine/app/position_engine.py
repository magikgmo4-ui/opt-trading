#!/usr/bin/env python3
"""
Position Engine Module
Manages state of trading positions (Paper Mode).

Usage:
    python -m modules.position_engine.app.position_engine [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/position"))

# --- Core Logic ---
class PositionEngine:
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

    def merge_data(self, execution, decisions, risk):
        """Merge data sources by symbol."""
        merged = {}
        
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(execution, "execution")
        merge_list(decisions, "decision")
        merge_list(risk, "risk")
        
        return merged

    def derive_position_state(self, symbol, data):
        """Derive position state from execution plan and constraints."""
        
        exe = data.get("execution", {})
        dec = data.get("decision", {})
        rsk = data.get("risk", {})
        
        exe_status = exe.get("execution_status", "BLOCKED")
        action = exe.get("action", "NO_ACTION")
        size_hint = exe.get("size_hint", "NONE")
        max_risk_pct = exe.get("max_risk_pct", 0.0)
        
        risk_status = rsk.get("risk_status", "BLOCK")
        
        # Defaults
        position_status = "FLAT"
        position_mode = "PAPER"
        side = "NONE"
        state = "NO_POSITION"
        next_action = "NO_ACTION"
        rationale = []
        
        # Logic
        if exe_status == "READY":
            if action == "PREPARE_LONG":
                position_status = "OPEN_CANDIDATE"
                side = "LONG"
                state = "READY_TO_TRACK"
                next_action = "WAIT_FOR_FILL_SIMULATION"
                rationale.append(f"Ready to track LONG ({size_hint}).")
            elif action == "PREPARE_SHORT":
                position_status = "OPEN_CANDIDATE"
                side = "SHORT"
                state = "READY_TO_TRACK"
                next_action = "WAIT_FOR_FILL_SIMULATION"
                rationale.append(f"Ready to track SHORT ({size_hint}).")
            else:
                position_status = "HOLD"
                state = "REVIEW"
                next_action = "REVIEW_SIGNAL"
                rationale.append(f"Execution ready but action is {action}.")
        
        elif exe_status == "BLOCKED":
            position_status = "BLOCKED"
            state = "NO_POSITION"
            next_action = "NO_ACTION"
            rationale.append("Execution blocked.")
            
        elif exe_status == "HOLD":
            position_status = "HOLD"
            state = "REVIEW"
            next_action = "MONITOR"
            rationale.append("Execution on hold.")
            
        else:
            position_status = "FLAT"
            state = "NO_POSITION"
            next_action = "NO_ACTION"
            rationale.append("No active signal.")

        return {
            "symbol": symbol,
            "position_status": position_status,
            "position_mode": position_mode,
            "side": side,
            "size_hint": size_hint,
            "max_risk_pct": max_risk_pct,
            "state": state,
            "next_action": next_action,
            "rationale": "; ".join(rationale),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def build_positions(self, merged_data):
        positions = []
        for sym, data in merged_data.items():
            res = self.derive_position_state(sym, data)
            positions.append(res)
            
        # Sort: OPEN_CANDIDATE first
        status_map = {"OPEN_CANDIDATE": 3, "HOLD": 2, "FLAT": 1, "BLOCKED": 0}
        positions.sort(key=lambda x: status_map.get(x["position_status"], 0), reverse=True)
        return positions

    def run_build(self, execution_path, decisions_path, risk_path):
        e_data = self.load_input(execution_path)
        d_data = self.load_input(decisions_path)
        r_data = self.load_input(risk_path)
        
        merged = self.merge_data(e_data, d_data, r_data)
        positions = self.build_positions(merged)
        
        print(json.dumps(positions, indent=2))
        return positions

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_build(
            CONFIG_DIR / "sample_execution.json",
            CONFIG_DIR / "sample_decisions.json",
            CONFIG_DIR / "sample_risk.json"
        )

    def export_results(self, positions=None, output_path=None):
        if not positions:
            positions = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"positions_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(positions, f, indent=2)
        print(f"Exported positions to: {output_path}")

    def explain_results(self, execution_path, decisions_path, risk_path):
        positions = self.run_build(execution_path, decisions_path, risk_path)
        print("\n=== Position Engine Explanation ===\n")
        print("Mode: PAPER ONLY (State Tracking)\n")
        
        for item in positions:
            print(f"Symbol: {item['symbol']}")
            print(f"  Status: {item['position_status']} ({item['side']})")
            print(f"  State: {item['state']} -> {item['next_action']}")
            print(f"  Rationale: {item['rationale']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Position Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    build_parser = subparsers.add_parser("build", help="Build position states")
    build_parser.add_argument("--execution", help="Execution results JSON")
    build_parser.add_argument("--decisions", help="Decision results JSON")
    build_parser.add_argument("--risk", help="Risk results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--execution", help="Execution results JSON")
    exp_parser.add_argument("--decisions", help="Decision results JSON")
    exp_parser.add_argument("--risk", help="Risk results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain position logic")
    explain_parser.add_argument("--execution", help="Execution results JSON")
    explain_parser.add_argument("--decisions", help="Decision results JSON")
    explain_parser.add_argument("--risk", help="Risk results JSON")

    args = parser.parse_args()
    engine = PositionEngine()

    if args.command == "status":
        print("Position Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
        print("Mode: PAPER ONLY")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "build":
        # Use provided args or defaults
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        engine.run_build(exe, dec, risk)
    elif args.command == "export":
        # Use provided args or defaults
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        positions = engine.run_build(exe, dec, risk)
        engine.export_results(positions, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        engine.explain_results(exe, dec, risk)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
