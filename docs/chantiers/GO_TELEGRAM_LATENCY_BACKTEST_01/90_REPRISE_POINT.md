---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_REPRISE_POINT
doc_type: reprise_point
repo: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 90_REPRISE_POINT - GO_TELEGRAM_LATENCY_BACKTEST_01

## Résumé

- telemetry JSONL enregistrée à chaque sendMessage (duration_ms + ok)
- outil offline de backtest latency (agrégation + percentiles)
- surfaces taggées via `source`

## Lecture minimale

1. `20_METHODOLOGY_AND_METRICS.md`
2. `30_BACKTEST_OUTPUT_SCHEMA.md`
3. `40_GAPS_AND_NEXT_GO.md`

## Vérif (local)

```powershell
python -m pytest tests\e2e\test_telegram_latency_backtest.py -q
```

## Next GO bundle

```text
GO_PERF_ENGINE_STRATEGY_SCORE_01
```
