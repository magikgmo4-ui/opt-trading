---
doc_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01_SWITCH_MATRIX
doc_type: switch_matrix
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01
status: draft_for_review
lifecycle_stage: child_switch_matrix
parent_go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - path-switch
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/01_SWITCH_MATRIX.md
point_de_reprise: "Lister les anciens chemins, nouveaux chemins, et impacts de bascule."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/00_CADRAGE.md
---

# 01_SWITCH_MATRIX

## 1_PATH MATRIX

| Surface | Ancien chemin | Nouveau chemin canonique | Action future |
|---|---|---|---|
| FastAPI app | `perf.perf_app:app` | `modules.perf.app:app` | switch optionnel |
| Perf engine | `modules.perf_engine.app.perf_engine` | `modules.perf.engine.app.perf_engine` | switch optionnel |
| Webhook adapter | `adapters.webhook_to_perf` | `modules.perf.webhook` | switch optionnel |
| DB path | `perf/perf.db` | inchangé dans ce lot | décision séparée |

## 2_AFFECTED REFERENCES

```text
- scripts/desk_pro_ui_toolbox_fix_cmd.sh
- scripts/desk_pro_ui_toolbox_final_cmd.sh
- modules/simex_bitget_bridge/cmd.sh
- scripts/verify_all.sh
- docs et scripts qui referencent perf/perf_app.py
```
