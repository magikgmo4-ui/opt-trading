# Stock True Value Layer

This module is the consolidated True Value layer for SpaceX Intelligence Final.

## Mode

Fixture-only and pure scoring in this bundle.

## Validate

```bash
python -m pytest tests/stock_true_value -q
python -m modules.stock_true_value.cli --fixture-only
```

## Outputs

```text
outputs/stock_true_value/latest/scores.json
outputs/stock_true_value/latest/summary.md
```
