# Decision Engine

The Decision Engine is the final logic layer before risk management. It synthesizes outputs from the `Opportunity Ranker`, `Probability Engine`, and `Liquidation Analyzer` to issue clear, actionable trading directives (`GO_LONG`, `GO_SHORT`, `WAIT`, `REJECT`).

## Purpose
- **Synthesize**: Combine ranked opportunities with detailed probability and liquidation data.
- **Decide**: Apply deterministic rules to validate setup quality.
- **Explain**: Provide a clear rationale for every decision.

## Structure
- `app/`: Python source code (`decision_engine.py`, `strategy_logic.py`).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for decision making.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Decide based on specific input files
./scripts/cmd.sh decide \
  --ranker config/sample_ranker.json \
  --probability config/sample_probability.json \
  --liquidations config/sample_liquidations.json

# Export decisions to JSON
./scripts/cmd.sh export --output data/decisions.json

# Explain the logic for a specific run (uses defaults if no args)
./scripts/cmd.sh explain
```

## Input Data
The engine expects three JSON lists:
1.  **Ranker**: `[{"symbol": "BTC", "opportunity_score": 0.8, "setup_bias": "LONG", ...}]`
2.  **Probability**: `[{"symbol": "BTC", "probability_long": 0.7, ...}]`
3.  **Liquidations**: `[{"symbol": "BTC", "liquidation_bias": "SHORTS_WIPED", ...}]`

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "decision": "GO_LONG",
    "confidence": 0.78,
    "decision_score": 0.81,
    "directional_bias": "LONG",
    "review_priority": "HIGH",
    "rationale": "Ranker high, probability supportive, liquidation profile not contradictory."
  }
]
```

## Future Integration
- **Upstream**: Consumes outputs from `Opportunity Ranker`, `Probability Engine`, `Liquidation Analyzer`.
- **Downstream**: Feeds `Risk Engine` (for sizing) and `Execution Engine` (for order placement).
