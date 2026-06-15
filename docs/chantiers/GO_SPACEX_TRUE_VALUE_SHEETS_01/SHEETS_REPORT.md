# SHEETS_REPORT — GO_SPACEX_TRUE_VALUE_SHEETS_01

## Phase 5 — Google Sheets

Export passif des scores vers Google Sheets — 1x/jour, dry-run par défaut.

## Changes

### `modules/stock_true_value/sheets_consumer.py`

| Aspect | Detail |
|---|---|
| Source | `outputs/stock_true_value/latest/scores.json` |
| Tab | `spacex_true_value` |
| Mode | `dry_run` by default |
| Activation | `python modules/stock_true_value/sheets_consumer.py --controlled-write` |
| Dependency | `SheetsWriter` from `modules.google_sheets_global_schema` |

### `modules/google_sheets_global_schema/validator.py`

| Addition | Detail |
|---|---|
| `spacex_true_value` | Added to `CANONICAL_TABS` |
| Schema columns | `as_of`, `ticker`, `grade`, `true_value_score`, `confidence_score` (required) |
| Schema optional | `hype_score`, `risk_score`, `action_bias`, `flags`, `source_ref` |
| PK | `(as_of, ticker)` |

### Column Mapping

| Sheets Column | Source Field |
|---|---|
| `as_of` | `scores.asof` (normalized to ISO UTC Z) |
| `ticker` | `item.ticker` |
| `grade` | `item.final_grade` |
| `true_value_score` | `item.true_value_score` |
| `hype_score` | `item.hype_score` |
| `risk_score` | `item.risk_score` |
| `confidence_score` | `item.confidence_score` |
| `action_bias` | `item.action_bias` |
| `flags` | `item.flags` (joined) |

### Dry-Run Validation

```
Tab: spacex_true_value | Mode: dry_run | Rows: 3 | OK: True (validation PASS)
```

## Mode

- Dry-run by default (no writes without `--controlled-write`)
- Manual trigger only
- Requires `ALLOW_GOOGLE_SHEETS_API_WRITE=1` + `GOOGLE_SHEETS_SYNC_SHEET_ID` for real writes

## Verdict

**PASS** — Sheets consumer ready. Dry-run validates 3 rows with correct schema.

## Next

Phase 6 — `GO_SPACEX_TRUE_VALUE_LIVE_COLLECTORS_01`
