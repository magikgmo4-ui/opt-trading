#!/usr/bin/env python3
"""
Portfolio Engine Module
Aggregates and tracks overall portfolio state.

Usage:
    python -m modules.portfolio_engine.app.portfolio_engine [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/portfolio"))

# --- Core Logic ---
class PortfolioEngine:
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

    def merge_data(self, positions, perf, risk, journal):
        """Merge data sources by symbol."""
        merged = {}
        
        def merge_list(source_list, source_name):
            for item in source_list:
                sym = item.get("symbol")
                if not sym: continue
                if sym not in merged: merged[sym] = {"symbol": sym}
                merged[sym][source_name] = item

        merge_list(positions, "position")
        merge_list(perf, "perf")
        merge_list(risk, "risk")
        merge_list(journal, "journal")
        
        return merged

    def build_portfolio_view(self, merged_data):
        """Construct the consolidated portfolio view."""
        
        symbol_rows = []
        
        # Metrics
        total_symbols = 0
        active_candidates = 0
        blocked_symbols = 0
        long_candidates = 0
        short_candidates = 0
        tracking_symbols = 0
        total_max_risk_pct = 0.0
        
        for sym, data in merged_data.items():
            total_symbols += 1
            
            pos = data.get("position", {})
            prf = data.get("perf", {})
            rsk = data.get("risk", {})
            jrn = data.get("journal", {})
            
            pos_status = pos.get("position_status", "FLAT")
            side = pos.get("side", "NONE")
            max_risk = pos.get("max_risk_pct", 0.0)
            
            perf_status = prf.get("perf_status", "INACTIVE")
            risk_status = rsk.get("risk_status", "BLOCK")
            desk_state = jrn.get("desk_state", "INACTIVE")
            
            # Row Data
            row = {
                "symbol": sym,
                "side": side,
                "position_status": pos_status,
                "perf_status": perf_status,
                "risk_status": risk_status,
                "desk_state": desk_state,
                "max_risk_pct": max_risk
            }
            symbol_rows.append(row)
            
            # Aggregation Logic
            if pos_status == "OPEN_CANDIDATE" or perf_status == "TRACKING":
                active_candidates += 1
                total_max_risk_pct += max_risk
                
                if side == "LONG":
                    long_candidates += 1
                elif side == "SHORT":
                    short_candidates += 1
                    
            if perf_status == "TRACKING":
                tracking_symbols += 1
                
            if risk_status == "BLOCK" or pos_status == "BLOCKED":
                blocked_symbols += 1

        # Profile Logic
        exposure_profile = "FLAT"
        if active_candidates > 0:
            if long_candidates > short_candidates:
                exposure_profile = "LONG_BIASED"
            elif short_candidates > long_candidates:
                exposure_profile = "SHORT_BIASED"
            elif long_candidates == short_candidates:
                exposure_profile = "BALANCED_LONG_SHORT"
            else:
                exposure_profile = "MIXED"
                
        # State Logic
        portfolio_state = "IDLE"
        if active_candidates > 0:
            portfolio_state = "ACTIVE"
            if blocked_symbols > 0:
                # Still active, but note blocks exists (normal)
                pass
        elif blocked_symbols == total_symbols and total_symbols > 0:
            portfolio_state = "BLOCKED"
            
        summary = (f"Portfolio {portfolio_state.lower()} with {active_candidates} active candidates "
                   f"({tracking_symbols} tracking), {exposure_profile.lower().replace('_', ' ')} exposure.")

        return {
            "portfolio_timestamp": datetime.now(timezone.utc).isoformat(),
            "portfolio_mode": "PAPER",
            "total_symbols": total_symbols,
            "active_candidates": active_candidates,
            "blocked_symbols": blocked_symbols,
            "long_candidates": long_candidates,
            "short_candidates": short_candidates,
            "tracking_symbols": tracking_symbols,
            "total_max_risk_pct": round(total_max_risk_pct, 2),
            "exposure_profile": exposure_profile,
            "portfolio_state": portfolio_state,
            "summary": summary,
            "symbol_rows": symbol_rows
        }

    def run_build(self, pos_path, perf_path, risk_path, journal_path):
        p_data = self.load_input(pos_path)
        f_data = self.load_input(perf_path)
        r_data = self.load_input(risk_path)
        j_data = self.load_input(journal_path)
        
        merged = self.merge_data(p_data, f_data, r_data, j_data)
        portfolio = self.build_portfolio_view(merged)
        
        print(json.dumps(portfolio, indent=2))
        return portfolio

    def run_sample(self):
        """Run with internal sample files."""
        return self.run_build(
            CONFIG_DIR / "sample_positions.json",
            CONFIG_DIR / "sample_perf.json",
            CONFIG_DIR / "sample_risk.json",
            CONFIG_DIR / "sample_journal.json"
        )

    def export_results(self, portfolio=None, output_path=None):
        if not portfolio:
            portfolio = self.run_sample()
            
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"portfolio_state_{ts}.json"
            
        with open(output_path, "w") as f:
            json.dump(portfolio, f, indent=2)
        print(f"Exported portfolio state to: {output_path}")

    def explain_results(self, pos_path, perf_path, risk_path, journal_path):
        portfolio = self.run_build(pos_path, perf_path, risk_path, journal_path)
        print("\n=== Portfolio Engine Explanation ===\n")
        print(f"State: {portfolio['portfolio_state']}")
        print(f"Exposure: {portfolio['exposure_profile']}")
        print(f"Risk Load: {portfolio['total_max_risk_pct']}%")
        print(f"Summary: {portfolio['summary']}\n")
        
        print("Details:")
        for row in portfolio['symbol_rows']:
            print(f"  {row['symbol']}: {row['side']} | {row['position_status']} | Risk={row['risk_status']}")
        print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Portfolio Engine")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with sample data")
    
    build_parser = subparsers.add_parser("build", help="Build portfolio view")
    build_parser.add_argument("--positions", help="Position results JSON")
    build_parser.add_argument("--perf", help="Perf results JSON")
    build_parser.add_argument("--risk", help="Risk results JSON")
    build_parser.add_argument("--journal", help="Journal results JSON")
    
    exp_parser = subparsers.add_parser("export", help="Export results")
    exp_parser.add_argument("--positions", help="Position results JSON")
    exp_parser.add_argument("--perf", help="Perf results JSON")
    exp_parser.add_argument("--risk", help="Risk results JSON")
    exp_parser.add_argument("--journal", help="Journal results JSON")
    exp_parser.add_argument("--output", help="Output file path")

    explain_parser = subparsers.add_parser("explain", help="Explain portfolio logic")
    explain_parser.add_argument("--positions", help="Position results JSON")
    explain_parser.add_argument("--perf", help="Perf results JSON")
    explain_parser.add_argument("--risk", help="Risk results JSON")
    explain_parser.add_argument("--journal", help="Journal results JSON")

    args = parser.parse_args()
    engine = PortfolioEngine()

    if args.command == "status":
        print("Portfolio Engine Status: OK")
        print(f"Output Dir: {engine.output_dir}")
    elif args.command == "sample":
        engine.run_sample()
    elif args.command == "build":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        perf = args.perf if args.perf else CONFIG_DIR / "sample_perf.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        jrn = args.journal if args.journal else CONFIG_DIR / "sample_journal.json"
        engine.run_build(pos, perf, risk, jrn)
    elif args.command == "export":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        perf = args.perf if args.perf else CONFIG_DIR / "sample_perf.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        jrn = args.journal if args.journal else CONFIG_DIR / "sample_journal.json"
        portfolio = engine.run_build(pos, perf, risk, jrn)
        engine.export_results(portfolio, output_path=args.output)
    elif args.command == "explain":
        # Use provided args or defaults
        pos = args.positions if args.positions else CONFIG_DIR / "sample_positions.json"
        perf = args.perf if args.perf else CONFIG_DIR / "sample_perf.json"
        risk = args.risk if args.risk else CONFIG_DIR / "sample_risk.json"
        jrn = args.journal if args.journal else CONFIG_DIR / "sample_journal.json"
        engine.explain_results(pos, perf, risk, jrn)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
