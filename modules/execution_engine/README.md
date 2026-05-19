# Execution Engine

The Execution Engine is the final stage of the Desk Pro pipeline. It translates risk-approved decisions into concrete execution plans.

## Purpose
- **Plan**: Convert `ALLOW` decisions into actionable execution steps (`PREPARE_LONG`, `PREPARE_SHORT`).
- **Route**: Assign an execution mode (currently `PAPER` only).
- **Block**: Enforce `BLOCK` or `NO_TRADE` directives from the Risk Engine.

## Structure
- `app/`: Python source code (planning logic).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for execution planning.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Generate execution plan based on specific input files
./scripts/cmd.sh plan \
  --decisions config/sample_decisions.json \
  --risk config/sample_risk.json

# Export execution plans to JSON
./scripts/cmd.sh export --output data/execution_plans.json

# Explain the logic for a specific run (uses defaults if no args)
./scripts/cmd.sh explain
```

## Input Data
The engine expects two JSON lists:
1.  **Decisions**: `[{"symbol": "BTC", "decision": "GO_LONG", ...}]`
2.  **Risk**: `[{"symbol": "BTC", "risk_status": "ALLOW", "max_risk_pct": 0.5, ...}]`

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "execution_status": "READY",
    "execution_mode": "PAPER",
    "action": "PREPARE_LONG",
    "size_hint": "HALF",
    "max_risk_pct": 0.5,
    "routing_hint": "paper-long",
    "rationale": "Decision GO_LONG and risk engine allows LONG_ONLY with medium sizing."
  }
]
```

## Future Integration
- **Upstream**: Consumes outputs from `Decision Engine` and `Risk Engine`.
- **Downstream**: Will feed the actual order router (CCXT/API) in future versions.
