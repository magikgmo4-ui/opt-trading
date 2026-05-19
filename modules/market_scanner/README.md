# Market Scanner

The Market Scanner is the entry point for opportunity detection in the Desk Pro system. It scans a universe of assets (from local files or mock data in v1) to identify potential trading setups based on technical scores.

## Purpose
- **Scan**: Filter a broad list of assets based on predefined criteria (Trend, Momentum, Volatility, Liquidity).
- **Rank**: Prioritize opportunities (High/Medium/Low) for the trader's attention.
- **Feed**: Produce structured output that can be consumed by the `Probability Engine` for deeper scoring.

## Structure
- `app/`: Python source code (scanning logic, ranking, normalization).
- `config/`: Configuration templates and sample market data.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for scanning and status.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Scan a specific input file
./scripts/cmd.sh scan --input config/sample_markets.json

# Export scan results to JSON
./scripts/cmd.sh export --output data/scan_results.json

# Explain the logic for a specific scan
./scripts/cmd.sh explain --input config/sample_markets.json
```

## Input Data (JSON)
The scanner expects a list of asset objects:
```json
[
  {
    "symbol": "BTCUSDT",
    "price": 91000,
    "trend_score": 0.7,
    "momentum_score": 0.5,
    "volatility_score": 0.4,
    "liquidity_score": 0.8
  }
]
```

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "scan_score": 0.74,
    "setup_bias": "LONG",
    "priority": "HIGH",
    "summary": "Strong trend, good liquidity, supportive open interest."
  }
]
```

## Future Integration
- **Upstream**: Will eventually connect to live market data feeds (CCXT, Coinglass).
- **Downstream**: Outputs are fed into `Probability Engine` and visualized in `Desk Pro Dashboard`.
