---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01_INBOX
doc_type: inbox_entry
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
created_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01

Child de `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01`.

Comble `liquidations_long` et `liquidations_short` sur Binance via `/fapi/v1/forceOrders`. Binance passe à couverture FULL (6/6).

Docs : `docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01/`
Code : `modules/derivatives_collector/app/binance_adapter.py`
Tests : `modules/derivatives_collector/tests/test_binance_liquidations_patch.py`
