---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_WRITER_ENRICH_PRODUCED_AT_01
created_at: 2026-05-28
---

# 40_GAPS_AND_NEXT_GO

## Gaps restants après ce GO

| Gap | Description |
|-----|-------------|
| GAP-M01 résolu | `market_metrics_writer` migré avec validation DC + manifest |
| GAP-P01 | `derivatives_collector__bitget` — `last_write: null` en prod |
| GAP-P02 | `derivatives_collector__binance` — idem |
| GAP-P04 | `coinglass` — `NOT_PROVEN_RUNTIME_ADAPTER` permanent |

## Prochain GO recommandé

`GO_OPT_TRADING_TELEGRAM_SCREENER_CHILD_RUNTIME_IMPL_01`

Transformer les specs parser/signal producer en code, produire des `signal_event`
compatibles Data Center.
