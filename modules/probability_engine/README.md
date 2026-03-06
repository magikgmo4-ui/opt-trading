# Probability Engine

The Probability Engine is the core scoring component of Desk Pro. It ingests normalized features from various collectors (market, derivatives, liquidation, regime) and produces a probabilistic directional bias (Long/Short) with confidence scores and explanations.

## Purpose
- **Centralized Scoring**: Aggregates disparate signals into a unified probability score.
- **Explainability**: Provides human-readable rationales for algorithmic decisions.
- **Extensibility**: Designed to easily add new feature inputs and weighting logic.

## Structure
- `app/`: Python source code (scoring logic, normalization, explanation).
- `config/`: Configuration templates (env.example) and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for testing and status.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and basic functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Score a specific input file
./scripts/cmd.sh score --input config/example_input.json

# Explain a specific input file (verbose)
./scripts/cmd.sh explain --input config/example_input.json
```

## Input Format (JSON)
```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-03-06T16:00:00Z",
  "trend_bias": 0.7,
  "momentum_bias": 0.4,
  "open_interest_bias": 0.6,
  "funding_bias": -0.2,
  "liquidation_bias": 0.3,
  "liquidity_bias": 0.5,
  "volatility_bias": 0.1,
  "regime_bias": 0.4
}
```

## Output Format (JSON)
```json
{
  "symbol": "BTCUSDT",
  "timestamp": "2026-03-06T16:00:00Z",
  "probability_long": 0.68,
  "probability_short": 0.32,
  "confidence": 0.61,
  "directional_bias": "LONG",
  "summary": "Bullish bias supported by trend, OI and liquidity; funding slightly negative."
}
```

## Future Integration
This module will feed into the `execution_engine` and `desk_pro_dashboard`.
