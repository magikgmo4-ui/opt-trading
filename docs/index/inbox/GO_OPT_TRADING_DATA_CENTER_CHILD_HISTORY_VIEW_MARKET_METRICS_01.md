---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01

Correction `perf_engine__replay_context` + verrouillage pattern `full_history` pour `market_metrics.v1`.

- **Chantier** : `docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_HISTORY_VIEW_MARKET_METRICS_01/`
- **Tests** : 135/135 PASS (+10 nouveaux)
- **Règle atteinte** : aucun consumer `market_metrics.v1` ne lit un `producer_id` path
- **Prochaine étape** : GO dédié si implémentation d'un consumer `not_started` réel
