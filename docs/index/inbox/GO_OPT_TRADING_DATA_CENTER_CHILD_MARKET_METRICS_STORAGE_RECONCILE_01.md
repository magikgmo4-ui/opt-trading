---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01_INBOX
doc_type: inbox
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01
status: open
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_MARKET_METRICS_STORAGE_RECONCILE_01 — inbox

## Rôle

Réconciliation : absorbe FAST_STORAGE_CACHE dans PF_DATA_CENTER, corrige le registry, étend le writer.

```text
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
BUNDLE_TARGET: MARKET_METRICS_STORAGE_RECONCILED_V1
```

## État

- `producers.json` : Bitget + Binance corrigés → full 6/6.
- `market_metrics_writer.py` : `write_market_metrics_to_data_center()` + `publish_market_metrics()` ajoutés.
- **53/53 tests PASS** (42 writer + 11 layout).
- FAST_STORAGE_CACHE absorbé — reprise annotée.
- BUNDLE_TARGET atteint.

## Règle canonique

```text
data/data_center/derivatives/<producer_id>/  <- source canonique
data/collectors/derivatives/                 <- legacy view
data/deskpro/inputs/market_metrics/          <- vue consumer Desk Pro (migration_needed)
```

## Prochain geste

```text
GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_TESTS_01
```
