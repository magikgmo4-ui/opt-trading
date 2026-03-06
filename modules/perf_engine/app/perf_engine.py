#!/usr/bin/env python3
"""
Perf Engine Module
Tracks performance of paper trading positions.

Usage:
    python -m modules.perf_engine.app.perf_engine [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/perf"))

# --- Core Logic ---
class PerfEngine:
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

    def merge_data(self, positions, execution):
        """Merge data sources by symbol."""
        merged = {}
        
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(positions, "position")
        merge_list(execution, "execution")
        
        return merged

    def track_symbol(self, symbol, data):
        """Derive performance state for a single symbol."""
        
        pos = data.get("position", {})
        exe = data.get("execution", {})
        
        pos_status = pos.get("position_status", "FLAT")
        side = pos.get("side", "NONE")
        size_hint = pos.get("size_hint", "NONE")
        max_risk_pct = pos.get("max_risk_pct", 0.0)
        pos_mode = pos.get("position_mode", "PAPER")
        
        exe_status = exe.get("execution_status", "BLOCKED")
        
        perf_status = "INACTIVE"
        tracking_mode = pos_mode
        pnl_status = "NO_POSITION"
        progress_state = "IDLE"
        rationale = []
        
        # Logic
        if pos_status == "OPEN_CANDIDATE" and exe_status == "READY":
            perf_status = "TRACKING"
            pnl_status = "OPEN_SIMULATED"
            progress_state = "AWAITING_MARK_TO_MARKET"
            rationale.append(f"Tracking {side} position ({size_hint}).")
            
        elif pos_status == "HOLD":
            perf_status = "WATCHLIST"
            pnl_status = "WATCHING"
            progress_state = "REVIEW"
            rationale.append("Watching symbol (Hold state).")
            
        elif pos_status == "BLOCKED":
            perf_status = "BLOCKED"
            pnl_status = "BLOCKED"
            progress_state = "BLOCKED"
            rationale.append("Symbol blocked.")
            
        else:
            perf_status = "INACTIVE"
            pnl_status = "NO_POSITION"
            progress_state = "IDLE"
            rationale.append("No active position.")

        return {
            "symbol": symbol,
            "perf_status": perf_status,
            "tracking_mode": tracking_mode,
            "side": side,
            "exposure_hint": size_hint,
            "max_risk_pct": max_risk_pct,
            "pnl_status": pnl_status,
            "progress_state": progress_state,
            "rationale": "; ".join(rationale),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    def track_performance(self, merged_data):
        states = []
        for sym, data in merged_data.items():
            res = self.track_symbol(sym, data)
            states.append(res)
            
        # Sort: TRACKING first
        status_map = {"TRACKING": 3, "WATCHLIST": 2, "INACTIVE": 1, "BLOCKED": 0}
        states.sort(key=lambda x: status_map.get(x["perf_status"], 0), reverse=True)
        return states

    def run_track(self, positions_path, execution_path):
        p_data = self.load_input(positions_path)
        e_data = self.load_input(execution_path)
        
        merged = self.merge_data(p_data, e_data)
        states = self.track_performance(merged)
        
        print(json.dumps(states, indent=2))
        return states

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_track(
            CONFIG_DIR / "sample_positions.json",
            CONFIG_DIR / "sample_execution.json"
        )

    def export_results(self, states=None, output_path=None):
        if not states:
            states = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"perf_states_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(states, f, indent=2)
        print(f"Exported performance states to: {output_path}")

    def explain_results(self, positions_path, execution_path):
        states = self.run_track(positions_path, execution_path)
        print("\n=== Perf Engine Explanation ===\n")
        print("Mode: PAPER ONLY (PnL Simulation)\n")
        
        for item in states:
            print(f"Symbol: {item['symbol']}")
            print(f"  Status: {item['perf_status']} ({item['pnl_status']})")
            print(f"  Progress: {item['progress_state']}")
            print(f"  Rationale: {item['rationale']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Perf Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    track_parser = subparsers.add_parser("track", help="Track performance")
    track_parser.add_argument("--positions", help="Position results JSON")
    track_parser.add_argument("--execution", help="Execution results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--positions", help="Position results JSON")
    exp_parser.add_argument("--execution", help="Execution results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain perf logic")
    explain_parser.add_argument("--positions", help="Position results JSON")
    explain_parser.add_argument("--execution", help="Execution results JSON")

    args = parser.parse_args()
    engine = PerfEngine()

    if args.command == "status":
        print("Perf Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
        print("Mode: PAPER ONLY")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "track":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        engine.run_track(pos, exe)
    elif args.command == "export":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        states = engine.run_track(pos, exe)
        engine.export_results(states, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        engine.explain_results(pos, exe)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
