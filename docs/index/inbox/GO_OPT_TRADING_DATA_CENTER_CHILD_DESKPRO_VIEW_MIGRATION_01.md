---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-23
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01

Migration Desk Pro → vue neutre Data Center `market_metrics.v1`.

- **Chantier** : `docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01/`
- **Reader** : `modules/desk_pro/service/market_metrics_reader.py`
- **Primary** : `data/data_center/views/market_metrics/latest.json`
- **Fallback** : `data/deskpro/inputs/market_metrics/latest.json`
- **Tests** : 119/119 PASS
- **`consumers.json`** : `desk_pro__market_metrics.migration_needed → false`
