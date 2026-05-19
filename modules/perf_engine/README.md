# Perf Engine

The Perf Engine tracks the performance of the Desk Pro system in simulation mode (Paper). It monitors the progression of trading ideas from candidate status to active tracking.

## Purpose
- **Track**: Monitor the lifecycle of paper positions.
- **Simulate**: Provide a "mock" PnL tracking state (Open/Closed).
- **Log**: Create a record of system activity for performance analysis.

## Structure
- `app/`: Python source code (tracking logic).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for performance tracking.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Track performance based on inputs
./scripts/cmd.sh track \
  --positions config/sample_positions.json \
  --execution config/sample_execution.json

# Export performance states to JSON
./scripts/cmd.sh export --output data/perf_states.json

# Explain the logic for a specific run (uses defaults if no args)
./scripts/cmd.sh explain
```

## Input Data
The engine expects two JSON lists:
1.  **Positions**: `[{"symbol": "BTC", "position_status": "OPEN_CANDIDATE", ...}]`
2.  **Execution**: `[{"symbol": "BTC", "execution_status": "READY", ...}]`

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "perf_status": "TRACKING",
    "tracking_mode": "PAPER",
    "side": "LONG",
    "exposure_hint": "HALF",
    "max_risk_pct": 0.5,
    "pnl_status": "OPEN_SIMULATED",
    "progress_state": "AWAITING_MARK_TO_MARKET",
    "rationale": "Position engine marked LONG open candidate and execution engine is READY in PAPER mode."
  }
]
```

## Future Integration
- **Upstream**: Consumes outputs from `Position Engine` and `Execution Engine`.
- **Downstream**: Feeds `Portfolio Engine`, `Journal Engine`, and `Desk Pro Dashboard`.
