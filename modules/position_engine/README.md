# Position Engine

The Position Engine manages the state of potential and active positions (Paper Mode). It bridges the gap between execution planning and portfolio tracking.

## Purpose
- **Track**: Monitor execution plans and convert them into position candidates.
- **State**: Maintain a clear state for each symbol (`READY_TO_TRACK`, `NO_POSITION`).
- **Bridge**: Prepare data for downstream performance tracking and portfolio management.

## Structure
- `app/`: Python source code (state management logic).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for position management.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Build position states based on inputs
./scripts/cmd.sh build \
  --execution config/sample_execution.json \
  --decisions config/sample_decisions.json \
  --risk config/sample_risk.json

# Export position states to JSON
./scripts/cmd.sh export --output data/positions.json

# Explain the logic for a specific run (uses defaults if no args)
./scripts/cmd.sh explain
```

## Input Data
The engine expects three JSON lists:
1.  **Execution**: `[{"symbol": "BTC", "execution_status": "READY", "action": "PREPARE_LONG", ...}]`
2.  **Decisions**: `[{"symbol": "BTC", "decision": "GO_LONG", ...}]`
3.  **Risk**: `[{"symbol": "BTC", "risk_status": "ALLOW", ...}]`

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "position_status": "OPEN_CANDIDATE",
    "position_mode": "PAPER",
    "side": "LONG",
    "size_hint": "HALF",
    "max_risk_pct": 0.5,
    "state": "READY_TO_TRACK",
    "next_action": "WAIT_FOR_FILL_SIMULATION",
    "rationale": "Execution engine marked READY PREPARE_LONG and risk settings allow a half-size long candidate."
  }
]
```

## Future Integration
- **Upstream**: Consumes outputs from `Execution Engine`, `Decision Engine`, `Risk Engine`.
- **Downstream**: Feeds `Portfolio Manager`, `Performance Tracker`, and `Desk Pro Dashboard`.
