# Journal Engine

The Journal Engine is the system of record for the Desk Pro. It aggregates the states from all upstream engines (Decision, Risk, Execution, Position, Perf) to create a comprehensive event log for each symbol.

## Purpose
- **Aggregate**: Collect the full context of a trade or setup.
- **Log**: Record the "Desk State" (Active Candidate, Blocked, Watchlist).
- **Archive**: Provide a structured history for post-trade analysis.

## Structure
- `app/`: Python source code (journaling logic).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for journaling.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Build journal entries based on inputs
./scripts/cmd.sh build \
  --decisions config/sample_decisions.json \
  --risk config/sample_risk.json \
  --execution config/sample_execution.json \
  --positions config/sample_positions.json \
  --perf config/sample_perf.json

# Export journal entries to JSON
./scripts/cmd.sh export --output data/journal_entries.json

# Explain the logic for a specific run (uses defaults if no args)
./scripts/cmd.sh explain
```

## Input Data
The engine expects five JSON lists:
1.  **Decisions**: `[{"symbol": "BTC", "decision": "GO_LONG", ...}]`
2.  **Risk**: `[{"symbol": "BTC", "risk_status": "ALLOW", ...}]`
3.  **Execution**: `[{"symbol": "BTC", "execution_status": "READY", ...}]`
4.  **Positions**: `[{"symbol": "BTC", "position_status": "OPEN_CANDIDATE", ...}]`
5.  **Perf**: `[{"symbol": "BTC", "perf_status": "TRACKING", ...}]`

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "journal_timestamp": "2026-03-06T18:15:00Z",
    "event_type": "DESK_STATE_UPDATE",
    "desk_state": "ACTIVE_LONG_CANDIDATE",
    "decision": "GO_LONG",
    "risk_status": "CAUTION",
    "execution_status": "READY",
    "position_status": "OPEN_CANDIDATE",
    "perf_status": "TRACKING",
    "summary": "Long candidate active: decision approved, risk cautious, execution ready, paper position tracked."
  }
]
```

## Future Integration
- **Upstream**: Consumes outputs from all major engines.
- **Downstream**: Feeds `Dashboard`, `Archive DB`, and `Reporting Tools`.
