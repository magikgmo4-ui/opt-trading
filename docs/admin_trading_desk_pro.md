# Admin Trading Desk Pro Integration

This pack provides the integration layer for the `admin-trading` machine (Linux Headless). It allows operators to run the Desk Pro system, view dashboards, and share results with other machines via the `/shared` mount.

## Installation

1.  Clone the repository on `admin-trading` (usually in `/opt/trading`).
2.  Run the installer (requires sudo for global wrappers):
    ```bash
    cd /opt/trading
    sudo ./scripts/admin_trading/desk_pro_install_admin_trading.sh
    ```

## Global Commands

After installation, the following commands are available globally:

- `desk-pro`: Main entry point (delegates to runner).
- `menu-desk_pro`: Interactive text menu.
- `sanity-desk_pro`: Health check script.

## Usage Guide

### 1. Daily Run
Run the full analysis pipeline and view the result:
```bash
desk-pro run-and-show
```

### 2. Check Status
See the current system state and last run info:
```bash
desk-pro status
```

### 3. Export & Share
Export the dashboard and copy artifacts to `/shared/desk_pro/latest`:
```bash
# 1. Export HTML report
desk-pro export-html-latest

# 2. Copy to shared drive
desk-pro copy-latest-to-shared
```

## Shared Directory Structure
The copy script populates `/shared/desk_pro/latest/` with:
- `run_summary.json`: High-level run stats.
- `portfolio_engine.json`: Consolidated portfolio state.
- `dashboard_latest.html`: Visual report (accessible by other machines).

## Architecture
- **Wrapper**: `desk_pro_cmd.sh` delegates to `modules.desk_pro_runner`.
- **Runner**: Orchestrates `desk_pro_orchestrator` and `desk_pro_dashboard`.
- **Engine**: Pure Python logic in `modules/`.
