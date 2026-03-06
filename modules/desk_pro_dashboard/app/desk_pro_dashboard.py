#!/usr/bin/env python3
"""
Desk Pro Dashboard Module
Aggregates and renders trading desk data from Desk Pro Orchestrator runs.

Usage:
    python -m modules.desk_pro_dashboard.app.desk_pro_dashboard [command] [args]
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

OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/dashboard"))
RUNS_DIR = PROJECT_ROOT / "data" / "desk_runs"

# --- Core Logic ---
class DeskProDashboard:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
        if not self.output_dir.exists():
            try:
                self.output_dir.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass

    def load_json(self, path):
        """Safely load JSON file."""
        p = Path(path)
        if not p.exists():
            return None
        try:
            with open(p, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load {path}: {e}")
            return None

    def find_latest_run(self):
        """Find the latest valid run directory."""
        if not RUNS_DIR.exists():
            return None
            
        # Find runs with run_summary.json
        valid_runs = []
        for d in RUNS_DIR.iterdir():
            if d.is_dir() and d.name.startswith("desk_run_"):
                if (d / "run_summary.json").exists():
                    valid_runs.append(d)
        
        if not valid_runs:
            return None
            
        # Sort by mtime, newest first
        valid_runs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return valid_runs[0]

    def aggregate_run_data(self, run_dir):
        """Aggregate data from a run directory into a dashboard view model."""
        run_path = Path(run_dir)
        
        # Load key files
        summary = self.load_json(run_path / "run_summary.json") or {}
        portfolio = self.load_json(run_path / "portfolio_engine.json") or {}
        journal = self.load_json(run_path / "journal_engine.json") or []
        perf = self.load_json(run_path / "perf_engine.json") or []
        
        # Build View Model
        view_model = {
            "run_id": summary.get("run_id", "UNKNOWN"),
            "run_timestamp": summary.get("run_timestamp", datetime.now(timezone.utc).isoformat()),
            "mode": summary.get("mode", "UNKNOWN"),
            "portfolio_state": portfolio.get("portfolio_state", "N/A"),
            "exposure_profile": portfolio.get("exposure_profile", "N/A"),
            "total_symbols": portfolio.get("total_symbols", 0),
            "active_candidates": portfolio.get("active_candidates", 0),
            "blocked_symbols": portfolio.get("blocked_symbols", 0),
            "tracking_symbols": portfolio.get("tracking_symbols", 0),
            "total_risk": portfolio.get("total_max_risk_pct", 0.0),
            "summary": portfolio.get("summary", "No portfolio summary available."),
            "rows": []
        }
        
        # Enrich rows from portfolio with journal/perf details if needed
        # For now, portfolio rows are quite complete
        if "symbol_rows" in portfolio:
            view_model["rows"] = portfolio["symbol_rows"]
        elif isinstance(journal, list) and journal:
            # Fallback to journal if portfolio missing
            view_model["rows"] = journal
            
        return view_model

    def render_terminal(self, data):
        """Render dashboard to terminal."""
        run_id = data.get("run_id", "SAMPLE")
        ts = data.get("run_timestamp", "N/A")
        mode = data.get("mode", "PAPER")
        
        print("\n" + "="*60)
        print(f" DESK PRO DASHBOARD | Run: {run_id}")
        print("="*60)
        print(f" Time: {ts} | Mode: {mode}")
        print("-" * 60)
        print(f" Portfolio State:  {data.get('portfolio_state')}")
        print(f" Exposure Profile: {data.get('exposure_profile')}")
        print(f" Risk Load:        {data.get('total_risk')}%")
        print("-" * 60)
        print(f" Active: {data.get('active_candidates')} | Tracking: {data.get('tracking_symbols')} | Blocked: {data.get('blocked_symbols')}")
        print("-" * 60)
        print(" SYMBOL STATUS:")
        print(f" {'SYMBOL':<10} | {'SIDE':<6} | {'POS STATUS':<15} | {'RISK':<8} | {'STATE'}")
        print("-" * 60)
        
        for row in data.get("rows", []):
            sym = row.get("symbol", "N/A")
            side = row.get("side", "-")
            pos = row.get("position_status", "N/A")
            rsk = row.get("risk_status", "N/A")
            state = row.get("desk_state", "N/A")
            print(f" {sym:<10} | {side:<6} | {pos:<15} | {rsk:<8} | {state}")
            
        print("-" * 60)
        print(f" SUMMARY: {data.get('summary')}")
        print("="*60 + "\n")

    def render_html(self, data):
        """Generate HTML representation."""
        rows_html = ""
        for row in data.get("rows", []):
            rows_html += f"""
            <tr>
                <td>{row.get('symbol')}</td>
                <td>{row.get('side')}</td>
                <td>{row.get('position_status')}</td>
                <td>{row.get('risk_status')}</td>
                <td>{row.get('desk_state')}</td>
            </tr>
            """
            
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Desk Pro Dashboard | {data.get('run_id')}</title>
            <style>
                body {{ font-family: monospace; background: #111; color: #eee; padding: 20px; }}
                .card {{ border: 1px solid #333; padding: 20px; max_width: 900px; margin: 0 auto; }}
                h1 {{ border-bottom: 1px solid #444; padding-bottom: 10px; }}
                .metric {{ display: flex; justify-content: space-between; margin: 5px 0; border-bottom: 1px solid #222; padding: 5px 0; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #333; }}
                th {{ color: #aaa; }}
                .ACTIVE {{ color: #0f0; }}
                .BLOCKED {{ color: #f00; }}
                .CAUTION {{ color: #fa0; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Desk Pro Dashboard</h1>
                <div class="metric"><span>Run ID:</span> <span>{data.get('run_id')}</span></div>
                <div class="metric"><span>Timestamp:</span> <span>{data.get('run_timestamp')}</span></div>
                <div class="metric"><span>Mode:</span> <span>{data.get('mode')}</span></div>
                <div class="metric"><span>State:</span> <span class="{data.get('portfolio_state')}">{data.get('portfolio_state')}</span></div>
                <div class="metric"><span>Exposure:</span> <span>{data.get('exposure_profile')}</span></div>
                <div class="metric"><span>Total Risk:</span> <span>{data.get('total_risk')}%</span></div>
                
                <div class="metric">
                    <span>Active: {data.get('active_candidates')}</span>
                    <span>Tracking: {data.get('tracking_symbols')}</span>
                    <span>Blocked: {data.get('blocked_symbols')}</span>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Side</th>
                            <th>Position</th>
                            <th>Risk</th>
                            <th>State</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
                
                <br/>
                <p><strong>Summary:</strong> {data.get('summary')}</p>
            </div>
        </body>
        </html>
        """
        return html

    def run_sample(self):
        """Run with internal sample data (Legacy Mode)."""
        sample_path = CONFIG_DIR / "sample_dashboard_input.json"
        if sample_path.exists():
            raw_data = self.load_json(sample_path)
            # Adapt legacy sample format to new view model if needed
            # For simplicity, we just wrap it or use it if it matches
            if "run_id" not in raw_data:
                # It's the old single-symbol format, adapt it
                data = {
                    "run_id": "SAMPLE_LEGACY",
                    "run_timestamp": raw_data.get("timestamp"),
                    "mode": "SAMPLE",
                    "portfolio_state": "SAMPLE",
                    "exposure_profile": raw_data.get("directional_bias"),
                    "total_risk": 0.0,
                    "active_candidates": 1,
                    "tracking_symbols": 0,
                    "blocked_symbols": 0,
                    "summary": raw_data.get("summary"),
                    "rows": [{
                        "symbol": raw_data.get("symbol"),
                        "side": raw_data.get("directional_bias"),
                        "position_status": "SAMPLE",
                        "risk_status": "SAMPLE",
                        "desk_state": "SAMPLE"
                    }]
                }
            else:
                data = raw_data
        else:
            data = {
                "run_id": "MOCK", 
                "run_timestamp": datetime.now(timezone.utc).isoformat(),
                "mode": "MOCK",
                "summary": "Mock data fallback."
            }
        self.render_terminal(data)
        return data

    def run_render_latest(self):
        """Find latest run and render it."""
        latest_run = self.find_latest_run()
        if not latest_run:
            print("No valid runs found in data/desk_runs/.")
            return None
        
        data = self.aggregate_run_data(latest_run)
        self.render_terminal(data)
        return data

    def run_render_run(self, run_dir):
        """Render a specific run directory."""
        p = Path(run_dir)
        if not p.exists() or not p.is_dir():
            print(f"Run directory not found: {run_dir}")
            return None
            
        data = self.aggregate_run_data(p)
        self.render_terminal(data)
        return data

    def export_json(self, data=None, output_path=None):
        if not data:
            # Default to latest run if available, else sample
            latest_run = self.find_latest_run()
            if latest_run:
                data = self.aggregate_run_data(latest_run)
            else:
                data = self.run_sample()
        
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"dashboard_{ts}.json"
        
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Exported JSON to: {output_path}")

    def export_html(self, data=None, output_path=None):
        if not data:
            # Default to latest run if available, else sample
            latest_run = self.find_latest_run()
            if latest_run:
                data = self.aggregate_run_data(latest_run)
            else:
                data = self.run_sample()
        
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"dashboard_{ts}.html"
            
        html_content = self.render_html(data)
        with open(output_path, "w") as f:
            f.write(html_content)
        print(f"Exported HTML to: {output_path}")

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Desk Pro Dashboard")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample", help="Run with legacy sample data")
    
    # New Commands
    subparsers.add_parser("render-latest", help="Render latest run")
    
    rr_parser = subparsers.add_parser("render-run", help="Render specific run")
    rr_parser.add_argument("--run-dir", required=True, help="Path to run directory")
    
    # Exports
    exp_json = subparsers.add_parser("export-json", help="Export JSON (default: latest)")
    exp_json.add_argument("--output", help="Path to output file")

    exp_html = subparsers.add_parser("export-html", help="Export HTML (default: latest)")
    exp_html.add_argument("--output", help="Path to output file")

    # Legacy aliases mapped to new logic
    subparsers.add_parser("export-json-latest", help="Alias for export-json")
    subparsers.add_parser("export-html-latest", help="Alias for export-html")

    args = parser.parse_args()
    dashboard = DeskProDashboard()

    if args.command == "status":
        print("Desk Pro Dashboard Status: OK")
        print(f"Output Dir: {dashboard.output_dir}")
        print(f"Runs Dir: {RUNS_DIR}")
    elif args.command == "sample":
        dashboard.run_sample()
    elif args.command == "render-latest":
        dashboard.run_render_latest()
    elif args.command == "render-run":
        dashboard.run_render_run(args.run_dir)
    elif args.command in ["export-json", "export-json-latest"]:
        dashboard.export_json(output_path=args.output if hasattr(args, 'output') else None)
    elif args.command in ["export-html", "export-html-latest"]:
        dashboard.export_html(output_path=args.output if hasattr(args, 'output') else None)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
