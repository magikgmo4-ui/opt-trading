---
doc_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - relocation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01/00_CADRAGE.md
point_de_reprise: "Planifier un éventuel déplacement de perf.db sans l'exécuter."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01

## 1_MASTER_TARGET

Planifier l’éventuel déplacement de `perf/perf.db` vers un emplacement plus explicite, sans toucher à la base ni au runtime dans ce GO.

## 2_RULE

```text
Le lot est un plan seulement.
Pas de déplacement effectif de DB.
Pas de changement de PERF_DB_PATH dans ce GO.
```

## 12_INVARIANTS

```text
- docs only
- 0 DB move
- 0 data mutation
- 0 runtime change
```
