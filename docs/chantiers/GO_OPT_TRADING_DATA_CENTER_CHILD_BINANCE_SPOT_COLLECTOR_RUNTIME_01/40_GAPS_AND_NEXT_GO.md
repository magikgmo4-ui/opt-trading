---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_BINANCE_SPOT_COLLECTOR_RUNTIME_01
status: open
created_at: 2026-05-28
updated_at: 2026-05-28
---

# 40_GAPS_AND_NEXT_GO

## Gaps restants après ce GO

| Gap | Description |
|-----|-------------|
| GAP-P03 résolu | Câblage `collector_binance_spot` → `data/data_center/spot/collector_binance_spot/` |
| GAP-M01 | `market_metrics_writer` pas encore migré / `enrich_produced_at()` pas standardisé |
| GAP-P01 | `derivatives_collector__bitget` — `last_write: null` en prod (pas de run réel) |
| GAP-P02 | `derivatives_collector__binance` — idem |
| GAP-P04 | `coinglass` — `NOT_PROVEN_RUNTIME_ADAPTER` permanent |

## Prochain GO recommandé

`GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01`

Objectif : migrer `market_metrics_writer`, ajouter/standardiser `enrich_produced_at()`,
aligner avec le schema `market_metrics.v1`, préserver la compatibilité des tests existants.
