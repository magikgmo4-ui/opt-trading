# DRYRUN_REPORT — GO_SPACEX_TRUE_VALUE_DRYRUN_OUTPUTS_01

## Phase 1 — Fixture Runtime

Dry-run du module `stock_true_value` depuis les fixtures uniquement.

## Command

```bash
python -m modules.stock_true_value.cli --fixture-only
```

## Output

```json
{"ok": true, "items": 3, "output": "outputs/stock_true_value/latest/scores.json"}
```

## Generated Files

| File | Size |
|---|---|
| `outputs/stock_true_value/latest/scores.json` | 3241 bytes |
| `outputs/stock_true_value/latest/summary.md` | 452 bytes |

## Schema Validation

| Check | Result |
|---|---|
| output.schema.json — top-level required fields | VALID |
| score_snapshot.schema.json — per-item required fields | VALID (3 items) |

## Scores Summary

| Ticker | Grade | True Value | Hype | Risk | Confidence |
|---|---|---|---|---|---|
| NVDA | B | 74.5 | 76.0 | 55.27 | 100.0 |
| MU | B | 75.0 | 58.0 | 42.18 | 100.0 |
| SPCX | RESEARCH_REQUIRED | 61.54 | 90.0 | 79.09 | 50.0 |

## Mode

- Fixture-only (no live collectors)
- No Data Center producer
- No LocalCMS consumer
- No Telegram alerts
- No broker/order execution

## Verdict

**PASS** — Dry-run outputs generated and validated. Ready for Phase 2 (Data Center Producer).

## Next

Phase 2 — `GO_SPACEX_TRUE_VALUE_DATACENTER_PRODUCER_01`
