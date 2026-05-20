---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_GAPS_AND_NEXT_GO
doc_type: gaps
repo: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 40_GAPS_AND_NEXT_GO

## Gaps

| Gap | Impact | Next step |
| --- | --- | --- |
| Pas de latence “réception client” | pas de true end-to-end | ajouter capture inbound plus tard (opt-in) |
| Pas de retry policy standard | timeouts/erreurs instables | définir policy par tier (ops/alerts/trading) |
| Pas de lien avec Perf Engine | pas de scoring promotion | brancher metrics latency vers perf |
| Pas d’export Sheets | pas de reporting transverse | writer controlled pour tab perf |

## Next GO bundle

```text
GO_PERF_ENGINE_STRATEGY_SCORE_01
```
