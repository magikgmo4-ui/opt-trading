---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-25
updated_at: 2026-05-25
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
links:
  - modules/data_center/spot_snapshot_dc_writer.py
  - modules/desk_pro/service/spot_snapshot_reader.py
  - modules/data_center/tests/test_spot_snapshot_dc_writer.py
  - tests/test_desk_pro_spot_snapshot_reader.py
  - modules/data_center/registry/consumers.json
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01

## Objet

Câbler le flux `pair_market_snapshot.v1` complet entre `collector_binance_spot`
et le consumer Desk Pro, via les chemins canoniques DC :

```
collector_binance_spot (normalized payload)
  → data/data_center/spot/collector_binance_spot/latest.json  (producer path)
  → data/data_center/views/pair_market_snapshot/latest.json   (consumer view)
  → data/data_center/views/pair_market_snapshot/by_symbol/    (per-symbol)
  → desk_pro service spot_snapshot_reader.py                  (consumer)
```

## Ce que ce GO ne fait PAS

- Ne modifie pas `collector_binance_spot` runtime (pas d'appel Binance live).
- Ne fait aucun appel API externe.
- Ne modifie pas les producers existants derivatives_collector.
- Ne ferme pas PF_DATA_CENTER.

## BUNDLE_TARGET

- [x] `spot_snapshot_dc_writer.py` — bridge payload → producer path + view + registry
- [x] `spot_snapshot_reader.py` — reader Desk Pro read-only depuis DC view
- [x] 10 tests writer + 8 tests reader = **18/18 PASS** + DC suite **97/97 PASS**
- [x] `consumers.json` : `desk_pro__spot_snapshot` → `implemented`
- [x] Contract test mis à jour pour refléter le reader implémenté
- [x] Sanity check PASS — 3 consumers implemented
