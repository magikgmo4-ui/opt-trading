# Opportunity Ranker

The Opportunity Ranker is the central aggregation module of the Desk Pro system. It fuses data from the `Market Scanner`, `Probability Engine`, and `Liquidation Analyzer` to produce a final, prioritized list of trading opportunities.

## Purpose
- **Fuse**: Merge disparate signals by symbol.
- **Score**: Calculate a unified `opportunity_score` (0.0 - 1.0).
- **Rank**: Sort opportunities by score and assign priority tiers (High/Medium/Low).

## Structure
- `app/`: Python source code (merging, scoring, ranking).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for ranking.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Rank specific input files
./scripts/cmd.sh rank \
  --scanner config/sample_scanner.json \
  --liquidations config/sample_liquidations.json \
  --probability config/sample_probability.json

# Export ranked results to JSON
./scripts/cmd.sh export --output data/ranked_opportunities.json

# Explain the logic for a specific rank run
./scripts/cmd.sh explain --scanner ...

# Explain logic using default sample inputs
./scripts/cmd.sh explain
```

## Input Data
The ranker expects three JSON lists:
1.  **Scanner**: `[{"symbol": "BTC", "scan_score": 0.8, ...}]`
2.  **Liquidations**: `[{"symbol": "BTC", "liquidation_score": -0.5, ...}]`
3.  **Probability**: `[{"symbol": "BTC", "probability_long": 0.7, "confidence": 0.6, ...}]`

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "opportunity_score": 0.81,
    "rank": 1,
    "priority": "HIGH",
    "setup_bias": "LONG",
    "confidence": 0.72,
    "summary": "High-ranked long opportunity supported by scan strength, bullish probability, and supportive liquidation profile."
  }
]
```

## Future Integration
- **Upstream**: Consumes outputs from `Market Scanner`, `Liquidation Analyzer`, `Probability Engine`.
- **Downstream**: Feeds `Desk Pro Dashboard` and eventually the `Execution Engine`.
