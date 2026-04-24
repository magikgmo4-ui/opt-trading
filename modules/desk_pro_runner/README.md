# Desk Pro Runner

The Desk Pro Runner is the operational entry point for the Desk Pro trading system. It provides a simple command-line interface to orchestrate runs, view dashboards, and check system status.

## Purpose
- **Simplify**: Single entry point for daily operations.
- **Integrate**: Connects Orchestrator (execution) and Dashboard (visualization).
- **Report**: Provides quick status checks and export capabilities.

## Structure
- `app/`: Python source code (runner logic).
- `config/`: Configuration templates.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for all runner operations.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check overall system status
./scripts/cmd.sh status

# Run a full orchestration (standard config)
./scripts/cmd.sh run

# Run orchestration and immediately show the dashboard
./scripts/cmd.sh run-and-show

# Show the dashboard for the latest run
./scripts/cmd.sh dashboard-latest

# Export the latest run to JSON
./scripts/cmd.sh export-json-latest

# Export the latest run to HTML
./scripts/cmd.sh export-html-latest

# Explain the runner workflow
./scripts/cmd.sh explain
```

## Integration
- **Upstream**: Orchestrates `desk_pro_orchestrator` and `desk_pro_dashboard`.
- **Downstream**: Intended for use by human operators or cron jobs.

## Workflow
1.  **Run**: Trigger `desk_pro_orchestrator` to execute the pipeline.
2.  **View**: Trigger `desk_pro_dashboard` to render the results.
3.  **Export**: Save reports for archiving or distribution.

## Family status
- `desk_pro_runner` is the module-level operator facade of the Desk Pro stack
- the live admin wrapper remains `scripts/admin_trading/desk_pro_cmd.sh`
- it is not the sole survivor of the family; it sits above `desk_pro_orchestrator` and `desk_pro_dashboard`
