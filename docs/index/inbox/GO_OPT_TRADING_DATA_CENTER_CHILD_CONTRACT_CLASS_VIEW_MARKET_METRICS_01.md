---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01

Vue neutre `market_metrics.v1` — découplage consumer/producer dans PF_DATA_CENTER.

- **Chantier** : `docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_CONTRACT_CLASS_VIEW_MARKET_METRICS_01/`
- **Fichiers modifiés** : `market_metrics_writer.py`, `consumers.json`, `layout.py`, `test_market_metrics_writer.py`, `test_contract_tests.py`
- **Résultat** : 91/91 PASS
- **Décision** : consumers lisent `data/data_center/views/market_metrics/`, pas `derivatives/<producer_id>/`
