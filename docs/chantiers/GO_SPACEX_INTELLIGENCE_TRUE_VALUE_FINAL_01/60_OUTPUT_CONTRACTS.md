# 60_OUTPUT_CONTRACTS

## Canonical daily JSON

```json
{
  "asof": "2026-06-15T08:30:00-04:00",
  "model_version": "spacex_true_value_final_v1",
  "universe": "CORE_WATCHLIST_PRIORITY",
  "items": []
}
```

## Item contract

```json
{
  "ticker": "NVDA",
  "universe": "CORE_AI",
  "scores": {
    "catalyst_score": null,
    "ecosystem_score": 80,
    "fundamental_score": 90,
    "valuation_score": 55,
    "flow_score": 75,
    "surprise_score": 80,
    "hype_score": 70,
    "risk_score": 45,
    "confidence_score": 100,
    "true_value_score": 74,
    "final_score": 78
  },
  "final_grade": "A",
  "action_bias": "watchlist_monitor",
  "flags": [],
  "source_health": {
    "missing_sources": [],
    "stale_sources": [],
    "data_conflicts": []
  }
}
```

## Required fields

Every output item must include:

```text
ticker
asof
model_version
universe
true_value_score
hype_score
risk_score
confidence_score
final_grade
flags
source_health
```

## Markdown summary

```markdown
# SpaceX True Value Daily Summary

## A+ / A candidates
## High true value / high hype
## Dangerous speculation
## Surprise watch
## Low confidence / missing data
```

## Backtest contract

Future outputs:

```text
outputs/spacex_true_value/backtests/{ticker}/{model_version}.json
```

Forward returns:

```yaml
forward_returns:
  d1: float
  d5: float
  d20: float
  d60: float
```
