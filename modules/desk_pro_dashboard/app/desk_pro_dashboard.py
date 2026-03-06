#!/usr/bin/env python3
"""
Desk Pro Dashboard Module
Aggregates and renders trading desk data.

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

# --- Core Logic ---
class DeskProDashboard:
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
            return json.load(f)

    def render_terminal(self, data):
        """Render dashboard to terminal."""
        symbol = data.get("symbol", "UNKNOWN")
        ts = data.get("timestamp", "N/A")
        bias = data.get("directional_bias", "NEUTRAL")
        conf = data.get("confidence", 0.0)
        
        # Color codes (if supported, else plain)
        # Using simple markers for now
        bias_marker = "[+]" if bias == "LONG" else "[-]" if bias == "SHORT" else "[=]"
        
        print("\n" + "="*40)
        print(f" DESK PRO DASHBOARD | {symbol}")
        print("="*40)
        print(f" Time: {ts}")
        print("-" * 40)
        print(f" BIAS: {bias_marker} {bias} (Conf: {conf:.2f})")
        print(f" Prob Long:  {data.get('probability_long', 0.0):.2f}")
        print(f" Prob Short: {data.get('probability_short', 0.0):.2f}")
        print("-" * 40)
        print(" METRICS:")
        print(f"  Open Interest:   {data.get('open_interest', 'N/A')}")
        print(f"  Funding Rate:    {data.get('funding_rate', 'N/A')}")
        print(f"  L/S Ratio:       {data.get('long_short_ratio', 'N/A')}")
        print(f"  Liq Long/Short:  {data.get('liquidations_long', 'N/A')} / {data.get('liquidations_short', 'N/A')}")
        print("-" * 40)
        print(" SUMMARY:")
        print(f"  {data.get('summary', 'No summary available.')}")
        print("="*40 + "\n")

    def render_html(self, data):
        """Generate simple HTML representation."""
        symbol = data.get("symbol", "UNKNOWN")
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Desk Pro | {symbol}</title>
            <style>
                body {{ font-family: monospace; background: #111; color: #eee; padding: 20px; }}
                .card {{ border: 1px solid #333; padding: 20px; max_width: 600px; margin: 0 auto; }}
                h1 {{ border-bottom: 1px solid #444; padding-bottom: 10px; }}
                .metric {{ display: flex; justify-content: space-between; margin: 5px 0; }}
                .bias-LONG {{ color: #0f0; }}
                .bias-SHORT {{ color: #f00; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>{symbol} Dashboard</h1>
                <div class="metric"><span>Time:</span> <span>{data.get('timestamp')}</span></div>
                <div class="metric"><span>Bias:</span> <span class="bias-{data.get('directional_bias')}">{data.get('directional_bias')}</span></div>
                <div class="metric"><span>Confidence:</span> <span>{data.get('confidence')}</span></div>
                <hr/>
                <div class="metric"><span>Prob Long:</span> <span>{data.get('probability_long')}</span></div>
                <div class="metric"><span>Prob Short:</span> <span>{data.get('probability_short')}</span></div>
                <hr/>
                <div class="metric"><span>Open Interest:</span> <span>{data.get('open_interest')}</span></div>
                <div class="metric"><span>Funding:</span> <span>{data.get('funding_rate')}</span></div>
                <br/>
                <p><strong>Summary:</strong> {data.get('summary')}</p>
            </div>
        </body>
        </html>
        """
        return html

    def run_sample(self):
        """Run with internal sample data."""
        sample_path = CONFIG_DIR / "sample_dashboard_input.json"
        if sample_path.exists():
            data = self.load_input(sample_path)
        else:
            data = {
                "symbol": "MOCK", 
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "directional_bias": "NEUTRAL",
                "summary": "Mock data fallback."
            }
        self.render_terminal(data)
        return data

    def run_render(self, input_path):
        data = self.load_input(input_path)
        self.render_terminal(data)

    def export_json(self, input_path=None, output_path=None):
        data = self.load_input(input_path) if input_path else self.run_sample()
        
        if not output_path:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.output_dir / f"dashboard_{ts}.json"
        
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Exported JSON to: {output_path}")

    def export_html(self, input_path=None, output_path=None):
        data = self.load_input(input_path) if input_path else self.run_sample()
        
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
    subparsers.add_parser("sample", help="Run with sample data")
    
    render_parser = subparsers.add_parser("render", help="Render dashboard")
    render_parser.add_argument("--input", help="Path to input JSON")
    
    exp_json = subparsers.add_parser("export-json", help="Export JSON")
    exp_json.add_argument("--input", help="Path to input JSON")
    exp_json.add_argument("--output", help="Path to output file")

    exp_html = subparsers.add_parser("export-html", help="Export HTML")
    exp_html.add_argument("--input", help="Path to input JSON")
    exp_html.add_argument("--output", help="Path to output file")

    args = parser.parse_args()
    dashboard = DeskProDashboard()

    if args.command == "status":
        print("Desk Pro Dashboard Status: OK")
        print(f"Output Dir: {dashboard.output_dir}")
    elif args.command == "sample":
        dashboard.run_sample()
    elif args.command == "render":
        if args.input:
            dashboard.run_render(args.input)
        else:
            dashboard.run_sample()
    elif args.command == "export-json":
        dashboard.export_json(args.input, args.output)
    elif args.command == "export-html":
        dashboard.export_html(args.input, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
