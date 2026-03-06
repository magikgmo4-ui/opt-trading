#!/usr/bin/env python3
"""
Desk Pro Orchestrator
Executes the entire Desk Pro pipeline.

Usage:
    python -m modules.desk_pro_orchestrator.app.desk_pro_orchestrator [command] [args]
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

def get_output_dir(path_str):
    """Resolve output directory relative to project root if not absolute."""
    p = Path(path_str)
    if p.is_absolute():
        return p
    return PROJECT_ROOT / p

BASE_OUTPUT_DIR = get_output_dir(os.getenv("OUTPUT_DIR", "data/desk_runs"))

# --- Module Registry ---
# Maps module names to their python module path and main command
MODULE_REGISTRY = {
    "market_scanner": "modules.market_scanner.app.market_scanner",
    "liquidation_analyzer": "modules.liquidation_analyzer.app.liquidation_analyzer",
    "probability_engine": "modules.probability_engine.app.probability_engine",
    "opportunity_ranker": "modules.opportunity_ranker.app.opportunity_ranker",
    "decision_engine": "modules.decision_engine.app.decision_engine",
    "risk_engine": "modules.risk_engine.app.risk_engine",
    "execution_engine": "modules.execution_engine.app.execution_engine",
    "position_engine": "modules.position_engine.app.position_engine",
    "perf_engine": "modules.perf_engine.app.perf_engine",
    "journal_engine": "modules.journal_engine.app.journal_engine",
    "portfolio_engine": "modules.portfolio_engine.app.portfolio_engine"
}

# --- Core Logic ---
class DeskProOrchestrator:
    def __init__(self):
        self.run_timestamp = datetime.now(timezone.utc)
        self.run_id = f"desk_run_{self.run_timestamp.strftime('%Y%m%d_%H%M%S')}"
        self.run_dir = BASE_OUTPUT_DIR / self.run_id
        
        # Ensure run directory exists
        if not self.run_dir.exists():
            try:
                self.run_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Error creating run directory: {e}")
                sys.exit(1)

    def run_module(self, module_name, command, args=[]):
        """Execute a single module via subprocess."""
        module_path = MODULE_REGISTRY.get(module_name)
        if not module_path:
            return {"status": "SKIPPED", "error": "Module not found in registry"}

        print(f"  -> Running {module_name}...")
        
        # Prepare output file path for this module's result
        output_file = self.run_dir / f"{module_name}.json"
        
        # Construct command
        cmd = [sys.executable, "-m", module_path, command] + args
        
        # Add output argument if supported (most modules support --output for export command)
        # For sample/default runs, we might capture stdout instead
        # Here we assume 'sample' or 'run' commands print JSON to stdout
        
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=PROJECT_ROOT,
                check=False
            )
            
            if result.returncode != 0:
                return {"status": "FAILED", "error": result.stderr.strip()}
            
            # Save stdout to file
            with open(output_file, "w") as f:
                f.write(result.stdout)
                
            return {"status": "OK", "output_path": str(output_file)}
            
        except Exception as e:
            return {"status": "FAILED", "error": str(e)}

    def orchestrate_run(self, config_path=None):
        """Execute the full pipeline based on config."""
        
        # Load config
        if config_path:
            cfg_path = Path(config_path)
        else:
            cfg_path = CONFIG_DIR / "run_config.example.json"
            
        if not cfg_path.exists():
            print(f"Config not found: {cfg_path}")
            return
            
        with open(cfg_path, "r") as f:
            config = json.load(f)
            
        modules_to_run = config.get("modules", [])
        mode = config.get("mode", "PAPER")
        
        print(f"Starting Desk Pro Run: {self.run_id} (Mode: {mode})")
        print(f"Output Directory: {self.run_dir}")
        print("-" * 40)
        
        results = {
            "run_id": self.run_id,
            "run_timestamp": self.run_timestamp.isoformat(),
            "mode": mode,
            "modules_executed": [],
            "modules_ok": 0,
            "modules_failed": 0,
            "module_results": {}
        }
        
        for mod_cfg in modules_to_run:
            name = mod_cfg["name"]
            cmd = mod_cfg["command"]
            
            res = self.run_module(name, cmd)
            
            results["modules_executed"].append(name)
            results["module_results"][name] = res
            
            if res["status"] == "OK":
                results["modules_ok"] += 1
            else:
                results["modules_failed"] += 1
                print(f"    !! {name} FAILED: {res.get('error')}")
        
        # Generate Summary
        summary_file = self.run_dir / "run_summary.json"
        
        results["summary"] = (f"Desk Pro run completed. OK: {results['modules_ok']}, "
                              f"Failed: {results['modules_failed']}.")
                              
        with open(summary_file, "w") as f:
            json.dump(results, f, indent=2)
            
        print("-" * 40)
        print(f"Run Complete. Summary saved to: {summary_file}")
        print(results["summary"])
        
        return results

    def export_summary(self, output_path=None):
        """Find the latest valid run (with summary) and export it."""
        # Find runs dir
        if not BASE_OUTPUT_DIR.exists():
            print("No runs found (data directory missing).")
            return

        # List all run directories
        all_run_dirs = [d for d in BASE_OUTPUT_DIR.iterdir() if d.is_dir() and d.name.startswith("desk_run_")]
        
        # Filter for runs that actually have a summary file
        valid_runs = []
        for d in all_run_dirs:
            summary_file = d / "run_summary.json"
            if summary_file.exists():
                valid_runs.append(d)
        
        if not valid_runs:
            print("No valid runs found (no run_summary.json detected).")
            return

        # Sort by modification time, newest first
        valid_runs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
        latest_run = valid_runs[0]
        summary_file = latest_run / "run_summary.json"
            
        # Read summary
        with open(summary_file, "r") as f:
            summary_data = json.load(f)
            
        print(f"\n=== Latest Valid Run Summary ({latest_run.name}) ===\n")
        print(json.dumps(summary_data, indent=2))
        
        # Export if requested
        if output_path:
            out_p = Path(output_path)
            # Handle relative path
            if not out_p.is_absolute():
                out_p = PROJECT_ROOT / out_p
                
            # Ensure parent dir exists
            if not out_p.parent.exists():
                out_p.parent.mkdir(parents=True, exist_ok=True)
                
            with open(out_p, "w") as f:
                json.dump(summary_data, f, indent=2)
            print(f"\nSummary exported to: {out_p}")

    def explain_orchestration(self):
        print("\n=== Desk Pro Orchestrator Explanation ===\n")
        print("Pipeline Order:")
        for i, mod in enumerate(MODULE_REGISTRY.keys(), 1):
            print(f"  {i}. {mod}")
        print("\nLogic:")
        print("  - Creates a timestamped run directory.")
        print("  - Executes each module in sequence via subprocess.")
        print("  - Captures JSON output from stdout to file.")
        print("  - Generates a final run summary JSON.")
        print("-" * 30)

# --- CLI ---
def main():
    parser = argparse.ArgumentParser(description="Desk Pro Orchestrator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("status", help="Show module status")
    subparsers.add_parser("sample-run", help="Run a sample orchestration")
    
    run_parser = subparsers.add_parser("run", help="Run full orchestration")
    run_parser.add_argument("--config", help="Path to run config JSON")
    
    exp_parser = subparsers.add_parser("export-summary", help="Export summary of last run")
    exp_parser.add_argument("--output", help="Optional output path for summary JSON")
    
    subparsers.add_parser("explain", help="Explain orchestration logic")

    args = parser.parse_args()
    orchestrator = DeskProOrchestrator()

    if args.command == "status":
        print("Desk Pro Orchestrator Status: OK")
        print(f"Base Output Dir: {BASE_OUTPUT_DIR}")
        print(f"Modules Registered: {len(MODULE_REGISTRY)}")
    elif args.command == "sample-run":
        orchestrator.orchestrate_run()
    elif args.command == "run":
        orchestrator.orchestrate_run(config_path=args.config)
    elif args.command == "export-summary":
        # Export latest summary
        orchestrator.export_summary(output_path=args.output)
    elif args.command == "explain":
        orchestrator.explain_orchestration()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
