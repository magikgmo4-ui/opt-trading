---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01

Inventaire et verrouillage des consumers `latest_only` `market_metrics.v1`.

- **Chantier** : `docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_LATEST_CONSUMERS_VIEW_MIGRATION_01/`
- **Résultat** : 121/121 PASS (+2 tests invariants)
- **desk_pro** : migré (DONE) ; **telegram_screener**, **google_sheets** : not_started (aucun reader, pas de faux runtime)
- **Invariant figé** : aucun `latest_only` consumer ne référence un `producer_id`
