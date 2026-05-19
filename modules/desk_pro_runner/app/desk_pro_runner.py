#!/usr/bin/env python3
"""
Desk Pro Runner
Operational entry point for the Desk Pro system.

Usage:
    python -m modules.desk_pro_runner.app.desk_pro_runner [command] [args]
"""
import sys
import os
import json
import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# --- Configuration ---
MODULE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MODULE_DIR.parent.parent
CONFIG_DIR = MODULE_DIR / "config"

# Paths to other modules
ORCHESTRATOR_MOD = "modules.desk_pro_orchestrator.app.desk_pro_orchestrator"
DASHBOARD_MOD = "modules.desk_pro_dashboard.app.desk_pro_dashboard"
RUNS_DIR = PROJECT_ROOT / "data" / "desk_runs"

# --- Core Logic ---
class DeskProRunner:
    def __init__(self):
        pass

    def run_subprocess(self, module, command, args=[]):
        """Execute a module command via subprocess."""
        cmd = [sys.executable, "-m", module, command] + args
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=PROJECT_ROOT,
                check=False
            )
            return result
        except Exception as e:
            print(f"Error executing {module}: {e}")
            return None

    def get_status(self):
        """Check system status."""
        orchestrator_ok = False
        dashboard_ok = False
        latest_run_id = None
        
        # Check modules by dry-running status
        res_orch = self.run_subprocess(ORCHESTRATOR_MOD, "status")
        if res_orch and res_orch.returncode == 0:
            orchestrator_ok = True
            
        res_dash = self.run_subprocess(DASHBOARD_MOD, "status")
        if res_dash and res_dash.returncode == 0:
            dashboard_ok = True
            
        # Check latest run
        if RUNS_DIR.exists():
            runs = [d for d in RUNS_DIR.iterdir() if d.is_dir() and d.name.startswith("desk_run_")]
            valid_runs = [r for r in runs if (r / "run_summary.json").exists()]
            if valid_runs:
                valid_runs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                latest_run_id = valid_runs[0].name

        status = {
            "runner_status": "OK",
            "mode": "PAPER",
            "orchestrator_available": orchestrator_ok,
            "dashboard_available": dashboard_ok,
            "latest_run_available": latest_run_id is not None,
            "latest_run_id": latest_run_id,
            "summary": "Desk Pro runner ready."
        }
        
        print(json.dumps(status, indent=2))
        return status

    def run_orchestration(self):
        """Run the orchestrator."""
        print(">>> Starting Desk Pro Orchestration...")
        res = self.run_subprocess(ORCHESTRATOR_MOD, "run")
        if res and res.returncode == 0:
            print(">>> Orchestration Complete.")
            # Print last few lines of output which usually contain summary
            lines = res.stdout.strip().split('\n')
            print("\n".join(lines[-5:]))
            return True
        else:
            print(">>> Orchestration FAILED.")
            if res:
                print(res.stderr)
            return False

    def show_dashboard(self):
        """Show the dashboard for the latest run."""
        print(">>> Rendering Dashboard...")
        res = self.run_subprocess(DASHBOARD_MOD, "render-latest")
        if res and res.returncode == 0:
            print(res.stdout)
        else:
            print(">>> Dashboard render FAILED.")
            if res:
                print(res.stderr)

    def run_and_show(self):
        """Run orchestration and then show dashboard."""
        if self.run_orchestration():
            self.show_dashboard()

    def export_json_latest(self):
        """Export latest run to JSON via dashboard."""
        print(">>> Exporting JSON...")
        res = self.run_subprocess(DASHBOARD_MOD, "export-json")
        if res and res.returncode == 0:
            print(res.stdout.strip())
        else:
            print(">>> Export FAILED.")
            if res: print(res.stderr)

    def export_html_latest(self):
        """Export latest run to HTML via dashboard."""
        print(">>> Exporting HTML...")
        res = self.run_subprocess(DASHBOARD_MOD, "export-html")
        if res and res.returncode == 0:
            print(res.stdout.strip())
        else:
            print(">>> Export FAILED.")
            if res: print(res.stderr)

    def explain(self):
        print("\n=== Desk Pro Runner Workflow ===\n")
        print("1. Orchestration: Triggers `desk_pro_orchestrator` to run the analysis pipeline.")
        print("2. Visualization: Uses `desk_pro_dashboard` to render the results of the run.")
        print("3. Reporting: Supports exporting the dashboard state to JSON or HTML.")
        print("\nUse `run-and-show` for the standard daily workflow.")
        print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Desk Pro Runner")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Check system status")
    subparsers.add_parser("run", help="Run orchestration")
    subparsers.add_parser("run-and-show", help="Run orchestration and show dashboard")
    subparsers.add_parser("dashboard-latest", help="Show dashboard for latest run")
    subparsers.add_parser("export-json-latest", help="Export latest run to JSON")
    subparsers.add_parser("export-html-latest", help="Export latest run to HTML")
    subparsers.add_parser("explain", help="Explain workflow")

    args = parser.parse_args()
    runner = DeskProRunner()

    if args.command == "status":
        runner.get_status()
    elif args.command == "run":
        runner.run_orchestration()
    elif args.command == "run-and-show":
        runner.run_and_show()
    elif args.command == "dashboard-latest":
        runner.show_dashboard()
    elif args.command == "export-json-latest":
        runner.export_json_latest()
    elif args.command == "export-html-latest":
        runner.export_html_latest()
    elif args.command == "explain":
        runner.explain()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
