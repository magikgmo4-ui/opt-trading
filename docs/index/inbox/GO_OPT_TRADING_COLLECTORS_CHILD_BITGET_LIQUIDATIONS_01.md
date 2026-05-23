---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01_INBOX
doc_type: inbox_entry
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
created_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01

Child de `GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01`.

Comble `liquidations_long` et `liquidations_short` sur Bitget via `/api/v2/mix/market/liquidation-order`. Bitget passe à couverture FULL (6/6).

Docs : `docs/chantiers/GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LIQUIDATIONS_01/`
Code : `modules/derivatives_collector/app/bitget_adapter.py`
Tests : `modules/derivatives_collector/tests/test_bitget_liquidations_patch.py`
