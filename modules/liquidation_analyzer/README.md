# Liquidation Analyzer

The Liquidation Analyzer module monitors and interprets market liquidation data to detect directional bias and potential reversal setups.

## Purpose
- **Monitor**: Ingest liquidation volume for Longs and Shorts.
- **Analyze**: Calculate liquidation imbalance (bias) and relative intensity (vs Open Interest).
- **Signal**: Provide a structured output (`LONGS_WIPED`, `SHORTS_WIPED`) for the `Probability Engine`.

## Structure
- `app/`: Python source code (analysis logic, metrics, normalization).
- `config/`: Configuration templates and sample data.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for analysis.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Analyze a specific input file
./scripts/cmd.sh analyze --input config/sample_liquidations.json

# Export analysis results to JSON
./scripts/cmd.sh export --output data/liquidation_results.json

# Explain the logic for a specific analysis
./scripts/cmd.sh explain --input config/sample_liquidations.json
```

## Input Data (JSON)
The analyzer expects a list of asset objects with liquidation details:
```json
[
  {
    "symbol": "BTCUSDT",
    "liquidations_long": 1200000,
    "liquidations_short": 250000,
    "open_interest": 45000000
  }
]
```

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "liquidation_bias": "LONGS_WIPED",
    "liquidation_score": -0.68,
    "intensity": "HIGH",
    "dominant_side": "LONG",
    "summary": "Heavy long liquidations suggest downside flush and elevated bearish pressure."
  }
]
```

## Future Integration
- **Upstream**: Will connect to `Derivatives Collector` or direct exchange feeds.
- **Downstream**: Outputs feed into `Probability Engine` (as `liquidation_bias`) and `Desk Pro Dashboard`.
