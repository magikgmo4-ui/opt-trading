---
doc_id: GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01_IMPLEMENTATION_NOTES
doc_type: implementation_notes
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01
status: draft_for_review
lifecycle_stage: child_implementation_notes
parent_go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01/01_IMPLEMENTATION_NOTES.md
point_de_reprise: "Tracer les launchers PERF qui resolvent maintenant automatiquement le chemin DB."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_PATH_SWITCH_IMPL_01/00_CADRAGE.md
---

# 01_IMPLEMENTATION_NOTES

## 1_FICHIERS MODIFIES

```text
scripts/desk_pro_ui_toolbox_fix_cmd.sh
scripts/desk_pro_ui_toolbox_final_cmd.sh
modules/simex_bitget_bridge/cmd.sh
modules/perf/README.md
```

## 2_COMPORTEMENT

```text
Les launchers resolvent maintenant la DB dans cet ordre :
1. PERF_DB_PATH deja exporte
2. DB canonique si presente
3. DB legacy sinon
```

## 3_COMPATIBILITE

```text
Pas de rupture si la DB canonique n'existe pas.
Le runtime reste fonctionnel sur perf/perf.db.
```

## RISKS

- À qualifier.
