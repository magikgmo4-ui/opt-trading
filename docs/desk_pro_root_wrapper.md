# Desk Pro Root Wrapper

The Desk Pro Root Wrapper is a lightweight, cross-platform entry point for the Desk Pro trading system. It allows operators to launch the system directly from the repository root without navigating into module subdirectories.

## Purpose
- **Convenience**: Single command to run, status check, or export.
- **Abstraction**: Hides the underlying python module path (`python -m modules.desk_pro_runner.app.desk_pro_runner`).
- **Cross-Platform**: Supports both Linux (Bash) and Windows (PowerShell).

## Commands

### Linux / Bash
Located in `scripts/`:

```bash
# Check status
./scripts/desk_pro_root_cmd.sh status

# Run full pipeline
./scripts/desk_pro_root_cmd.sh run

# Run and show dashboard
./scripts/desk_pro_root_cmd.sh run-and-show

# Show latest dashboard
./scripts/desk_pro_root_cmd.sh dashboard-latest

# Exports
./scripts/desk_pro_root_cmd.sh export-json-latest
./scripts/desk_pro_root_cmd.sh export-html-latest

# Interactive Menu
./scripts/desk_pro_root_menu.sh
```

### Windows / PowerShell
Located in `scripts/`:

```powershell
# Check status
.\scripts\desk_pro_root.ps1 status

# Run full pipeline
.\scripts\desk_pro_root.ps1 run

# Run and show dashboard
.\scripts\desk_pro_root.ps1 run-and-show

# Show latest dashboard
.\scripts\desk_pro_root.ps1 dashboard-latest

# Exports
.\scripts\desk_pro_root.ps1 export-json-latest
.\scripts\desk_pro_root.ps1 export-html-latest
```

## Operator Workflow
1.  **Start of Day**: Run `run-and-show` to generate fresh analysis and view the dashboard.
2.  **Monitoring**: Use `dashboard-latest` to check the state periodically.
3.  **End of Day**: Use `export-html-latest` to save a daily report.

## Integration
- **Delegates to**: `modules.desk_pro_runner.app.desk_pro_runner`
- **Orchestrates**: `desk_pro_orchestrator` (via runner)
- **Visualizes**: `desk_pro_dashboard` (via runner)
