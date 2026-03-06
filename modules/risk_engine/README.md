# Risk Engine

The Risk Engine is the guardian of the Desk Pro system. It evaluates proposed trading decisions against strict risk parameters to determine if a trade is allowed, and if so, what size it should be.

## Purpose
- **Evaluate**: Check if a decision (`GO_LONG`, `GO_SHORT`) meets risk criteria.
- **Size**: Determine the appropriate position size (`FULL`, `HALF`, `MICRO`, `NONE`).
- **Protect**: Block trades that have weak signals or conflicting data.

## Structure
- `app/`: Python source code (risk logic, sizing rules).
- `config/`: Configuration templates and sample inputs.
- `scripts/`: Standard shell wrappers (`cmd.sh`, `menu.sh`, `sanity_check.sh`).

## Usage
Use the provided scripts in `scripts/`:
- `menu.sh`: Interactive menu for risk assessment.
- `cmd.sh`: CLI wrapper for automation.
- `sanity_check.sh`: Validate installation and functionality.

## CLI Commands
```bash
# Check module status
./scripts/cmd.sh status

# Run with sample data (mock)
./scripts/cmd.sh sample

# Assess risk based on specific input files
./scripts/cmd.sh assess \
  --decisions config/sample_decisions.json \
  --ranker config/sample_ranker.json \
  --probability config/sample_probability.json

# Export risk assessments to JSON
./scripts/cmd.sh export --output data/risk_assessments.json

# Explain the logic for a specific run (uses defaults if no args)
./scripts/cmd.sh explain
```

## Input Data
The engine expects three JSON lists:
1.  **Decisions**: `[{"symbol": "BTC", "decision": "GO_LONG", "confidence": 0.8, ...}]`
2.  **Ranker**: `[{"symbol": "BTC", "priority": "HIGH", ...}]`
3.  **Probability**: `[{"symbol": "BTC", "probability_long": 0.75, ...}]`

## Output Data (JSON)
```json
[
  {
    "symbol": "BTCUSDT",
    "risk_status": "ALLOW",
    "risk_tier": "MEDIUM",
    "max_risk_pct": 0.5,
    "sizing_hint": "HALF",
    "allowed_action": "LONG_ONLY",
    "invalidation_hint": "Invalidate if decision confidence drops below threshold or structure breaks.",
    "rationale": "Decision is GO_LONG with supportive rank/probability, but confidence is not extreme."
  }
]
```

## Future Integration
- **Upstream**: Consumes outputs from `Decision Engine`, `Opportunity Ranker`, `Probability Engine`.
- **Downstream**: Feeds `Execution Engine` (final order generation) and `Desk Pro Dashboard`.
