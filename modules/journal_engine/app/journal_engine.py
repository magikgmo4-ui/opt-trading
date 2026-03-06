#!/usr/bin/env python3
"""
Journal Engine Module
Aggregates desk state into comprehensive journal entries.

Usage:
    python -m modules.journal_engine.app.journal_engine [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/journal"))

# --- Core Logic ---
class JournalEngine:
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

    def merge_data(self, decisions, risk, execution, positions, perf):
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
        merge_list(execution, "execution")
        merge_list(positions, "position")
        merge_list(perf, "perf")
        
        return merged

    def build_entry(self, symbol, data):
        """Construct a journal entry for a single symbol."""
        
        dec = data.get("decision", {})
        rsk = data.get("risk", {})
        exe = data.get("execution", {})
        pos = data.get("position", {})
        prf = data.get("perf", {})
        
        # Extract states
        decision = dec.get("decision", "WAIT")
        risk_status = rsk.get("risk_status", "BLOCK")
        exe_status = exe.get("execution_status", "BLOCKED")
        pos_status = pos.get("position_status", "FLAT")
        perf_status = prf.get("perf_status", "INACTIVE")
        
        # Determine Desk State
        desk_state = "INACTIVE"
        summary = ""
        
        if pos_status == "OPEN_CANDIDATE" and exe_status == "READY":
            side = pos.get("side", "NONE")
            if side == "LONG":
                desk_state = "ACTIVE_LONG_CANDIDATE"
                summary = "Active LONG candidate: approved and tracking."
            elif side == "SHORT":
                desk_state = "ACTIVE_SHORT_CANDIDATE"
                summary = "Active SHORT candidate: approved and tracking."
        
        elif pos_status == "HOLD":
            desk_state = "WATCHLIST"
            summary = "On Watchlist: signal exists but action pending."
            
        elif risk_status == "BLOCK" or exe_status == "BLOCKED":
            desk_state = "BLOCKED"
            summary = f"Blocked: Risk={risk_status}, Exec={exe_status}."
            
        else:
            desk_state = "INACTIVE"
            summary = "Inactive: no actionable signal."

        return {
            "symbol": symbol,
            "journal_timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": "DESK_STATE_UPDATE",
            "desk_state": desk_state,
            "decision": decision,
            "risk_status": risk_status,
            "execution_status": exe_status,
            "position_status": pos_status,
            "perf_status": perf_status,
            "summary": summary
        }

    def build_journal(self, merged_data):
        entries = []
        for sym, data in merged_data.items():
            res = self.build_entry(sym, data)
            entries.append(res)
            
        # Sort by active state first
        state_map = {
            "ACTIVE_LONG_CANDIDATE": 4,
            "ACTIVE_SHORT_CANDIDATE": 4,
            "WATCHLIST": 3,
            "INACTIVE": 2,
            "BLOCKED": 1
        }
        entries.sort(key=lambda x: state_map.get(x["desk_state"], 0), reverse=True)
        return entries

    def run_build(self, dec_path, risk_path, exe_path, pos_path, perf_path):
        d_data = self.load_input(dec_path)
        r_data = self.load_input(risk_path)
        e_data = self.load_input(exe_path)
        p_data = self.load_input(pos_path)
        f_data = self.load_input(perf_path)
        
        merged = self.merge_data(d_data, r_data, e_data, p_data, f_data)
        entries = self.build_journal(merged)
        
        print(json.dumps(entries, indent=2))
        return entries

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_build(
            CONFIG_DIR / "sample_decisions.json",
            CONFIG_DIR / "sample_risk.json",
            CONFIG_DIR / "sample_execution.json",
            CONFIG_DIR / "sample_positions.json",
            CONFIG_DIR / "sample_perf.json"
        )

    def export_results(self, entries=None, output_path=None):
        if not entries:
            entries = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"journal_entries_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(entries, f, indent=2)
        print(f"Exported journal entries to: {output_path}")

    def explain_results(self, dec_path, risk_path, exe_path, pos_path, perf_path):
        entries = self.run_build(dec_path, risk_path, exe_path, pos_path, perf_path)
        print("\n=== Journal Engine Explanation ===\n")
        print("Aggregation of all Desk Pro states.\n")
        
        for item in entries:
            print(f"Symbol: {item['symbol']}")
            print(f"  State: {item['desk_state']}")
            print(f"  Details: Dec={item['decision']}, Risk={item['risk_status']}, Exec={item['execution_status']}")
            print(f"  Summary: {item['summary']}")
            print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Journal Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    build_parser = subparsers.add_parser("build", help="Build journal entries")
    build_parser.add_argument("--decisions", help="Decision results JSON")
    build_parser.add_argument("--risk", help="Risk results JSON")
    build_parser.add_argument("--execution", help="Execution results JSON")
    build_parser.add_argument("--positions", help="Position results JSON")
    build_parser.add_argument("--perf", help="Perf results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--decisions", help="Decision results JSON")
    exp_parser.add_argument("--risk", help="Risk results JSON")
    exp_parser.add_argument("--execution", help="Execution results JSON")
    exp_parser.add_argument("--positions", help="Position results JSON")
    exp_parser.add_argument("--perf", help="Perf results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain journal logic")
    explain_parser.add_argument("--decisions", help="Decision results JSON")
    explain_parser.add_argument("--risk", help="Risk results JSON")
    explain_parser.add_argument("--execution", help="Execution results JSON")
    explain_parser.add_argument("--positions", help="Position results JSON")
    explain_parser.add_argument("--perf", help="Perf results JSON")

    args = parser.parse_args()
    engine = JournalEngine()

    if args.command == "status":
        print("Journal Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "build":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        perf = args.perf if args.perf else CONFIG_DIR / "sample_perf.json"
        engine.run_build(dec, risk, exe, pos, perf)
    elif args.command == "export":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        perf = args.perf if args.perf else CONFIG_DIR / "sample_perf.json"
        entries = engine.run_build(dec, risk, exe, pos, perf)
        engine.export_results(entries, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        dec = args.decisions if args.decisions else CONFIG_DIR / "sample_decisions.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        exe = args.execution if args.execution else CONFIG_DIR / "sample_execution.json"
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        perf = args.perf if args.perf else CONFIG_DIR / "sample_perf.json"
        engine.explain_results(dec, risk, exe, pos, perf)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
