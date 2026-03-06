# Portfolio Engine

The Portfolio Engine aggregates all trading data to provide a consolidated view of the Desk Pro's state. It tracks exposure, active candidates, and overall risk profile.

## Purpose
- **Aggregate**: Consolidate Position, Perf, Risk, and Journal data.
- **Monitor**: Track total exposure and active symbol counts.
- **Report**: Generate a high-level portfolio summary.

## Structure
- `app/`: Python source code (aggregation logic).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for portfolio management.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Build portfolio view based on inputs
./scripts/cmd.sh build \
  --positions config/sample_positions.json \
  --perf config/sample_perf.json \
  --risk config/sample_risk.json \
  --journal config/sample_journal.json

# Export portfolio state to JSON
./scripts/cmd.sh export --output data/portfolio_state.json

# Explain the logic for a specific run (uses defaults if no args)
./scripts/cmd.sh explain
```

## Input Data
The engine expects four JSON lists:
1.  **Positions**: `[{"symbol": "BTC", "position_status": "OPEN_CANDIDATE", ...}]`
2.  **Perf**: `[{"symbol": "BTC", "perf_status": "TRACKING", ...}]`
3.  **Risk**: `[{"symbol": "BTC", "risk_status": "ALLOW", ...}]`
4.  **Journal**: `[{"symbol": "BTC", "desk_state": "ACTIVE_LONG_CANDIDATE", ...}]`

## Output Data (JSON)
```json
{
  "portfolio_timestamp": "2026-03-06T18:30:00Z",
  "portfolio_mode": "PAPER",
  "total_symbols": 3,
  "active_candidates": 2,
  "blocked_symbols": 1,
  "long_candidates": 1,
  "short_candidates": 1,
  "tracking_symbols": 2,
  "total_max_risk_pct": 0.75,
  "exposure_profile": "BALANCED_LONG_SHORT",
  "portfolio_state": "ACTIVE",
  "summary": "Portfolio active with 2 tracked candidates, balanced long/short exposure, and one blocked symbol.",
  "symbol_rows": [
    {
      "symbol": "BTCUSDT",
      "side": "LONG",
      "position_status": "OPEN_CANDIDATE",
      "perf_status": "TRACKING",
      "risk_status": "CAUTION",
      "desk_state": "ACTIVE_LONG_CANDIDATE",
      "max_risk_pct": 0.5
    }
  ]
}
```

## Future Integration
- **Upstream**: Consumes outputs from `Position`, `Perf`, `Risk`, `Journal` engines.
- **Downstream**: Feeds `Dashboard`, `Allocation Engine`, `Monitoring Tools`.
