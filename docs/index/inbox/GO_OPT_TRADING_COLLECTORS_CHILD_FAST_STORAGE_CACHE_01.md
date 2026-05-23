---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01_INDEX
doc_type: index_inbox
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: closed
lifecycle_stage: accepted
created_at: 2026-05-23
---

# Index — GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01

**Stockage rapide market_metrics.v1** — writer + cache by_symbol + surface Desk Pro read-only.

## Chantier

`docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_FAST_STORAGE_CACHE_01/`

## Livrables

| Fichier | Rôle |
|---|---|
| `market_metrics_writer.py` | 3 fonctions : latest, by_symbol, deskpro |
| `test_market_metrics_writer.py` | 25 tests unittest — PASS |

## Chemins produits

```text
data/collectors/derivatives/latest.json
data/collectors/derivatives/cache/by_symbol/<SYMBOL>.json
data/deskpro/inputs/market_metrics/latest.json
data/deskpro/inputs/market_metrics/by_symbol/<SYMBOL>.json
```

## Prochain GO

`GO_OPT_TRADING_COLLECTORS_CHILD_LIFECYCLE_WRITER_INTEGRATION_01`
