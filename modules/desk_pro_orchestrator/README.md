# Desk Pro Orchestrator

The Desk Pro Orchestrator is the conductor of the trading system. It executes the entire analysis, decision, and tracking pipeline in a deterministic sequence, managing data flow between modules.

## Purpose
- **Orchestrate**: Run all Desk Pro modules in the correct order.
- **Manage Data**: Route outputs from one module as inputs to the next.
- **Report**: Generate a consolidated run summary.

## Structure
- `app/`: Python source code (orchestration logic).
- `config/`: Run configuration templates.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for orchestration.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run a sample orchestration (using internal sample data for each module)
./scripts/cmd.sh sample-run

# Run a full orchestration (standard config)
./scripts/cmd.sh run

# Run with custom config
./scripts/cmd.sh run --config config/my_run.json

# Export the last run summary
./scripts/cmd.sh export-summary

# Explain the logic (uses defaults if no args)
./scripts/cmd.sh explain
```

## Pipeline Execution Flow
The orchestrator executes modules in this specific order:
1.  **Market Scanner** (Inputs -> Candidates)
2.  **Liquidation Analyzer** (Market Data -> Liq Bias)
3.  **Probability Engine** (Market Data -> Probabilities)
4.  **Opportunity Ranker** (Candidates + Liq + Prob -> Ranked Ops)
5.  **Decision Engine** (Ranked Ops + Prob + Liq -> Decisions)
6.  **Risk Engine** (Decisions + Ranker + Prob -> Risk Assessment)
7.  **Execution Engine** (Decisions + Risk -> Execution Plan)
8.  **Position Engine** (Execution + Decisions + Risk -> Position State)
9.  **Perf Engine** (Positions + Execution -> Performance State)
10. **Journal Engine** (All States -> Journal Entries)
11. **Portfolio Engine** (All States -> Portfolio View)

## Output Data (Run Summary)
```json
{
  "run_id": "desk_run_20260306_181500",
  "run_timestamp": "2026-03-06T18:15:00Z",
  "mode": "PAPER",
  "modules_executed": ["market_scanner", "liquidation_analyzer", ...],
  "modules_ok": 11,
  "modules_failed": 0,
  "final_outputs": {
    "portfolio": "data/desk_runs/.../portfolio_state.json",
    "journal": "data/desk_runs/.../journal_entries.json"
  },
  "summary": "Desk Pro run completed successfully in PAPER mode."
}
```

## Future Integration
- **Upstream**: Triggered by Cron, Admin Dashboard, or Manual Event.
- **Downstream**: Pushes final state to Dashboard, Database, and Notification Services.

## Family status
- `desk_pro_orchestrator` is the execution backbone of the Desk Pro stack
- it is not an isolated survivor; it works under `desk_pro_runner` and with `desk_pro_dashboard`
