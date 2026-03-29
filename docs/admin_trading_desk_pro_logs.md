# Admin Trading Desk Pro Logs

This guide explains how to use the logging and archival features of the Desk Pro system on the `admin-trading` machine.

## Overview

The logging system captures the output of Desk Pro runs, timestamps them, and provides tools to review the execution history.

## Commands

### 1. Run with Logging
Execute a full run and save the output to a log file:
```bash
desk-pro-run-logged
# OR
desk-pro run-logged
```
This creates a log file in `data/logs/desk_pro/` and updates the `latest.log` symlink.

### 2. View Latest Log
See the tail of the most recent execution log:
```bash
desk-pro-tail-log
# OR
desk-pro tail-latest-log
```

### 3. Last Run Info
Get a quick summary of the last execution state (Orchestrator + Logs):
```bash
desk-pro-last-run
# OR
desk-pro last-run-info
```

## Directory Structure

Logs are stored in:
`data/logs/desk_pro/`

- `run_YYYYMMDD_HHMMSS.log`: Timestamped execution log.
- `latest.log`: Symlink to the most recent log file.

## Integration

- **Wrappers**: All log commands are integrated into `desk_pro_cmd.sh` and the interactive menu (`menu-desk_pro`).
- **Global Access**: Installing via `desk_pro_install_admin_trading.sh` creates global symlinks in `/usr/local/bin`.
