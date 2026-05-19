---
doc_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
topic_keys:
  - opt-trading
  - perf
  - restructure
  - plan
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_PLAN_01/00_CADRAGE.md
point_de_reprise: "Planifier la restructuration physique du cluster PERF sans l'executer."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/03_PERF_RESTRUCTURE_GAPS.md
---

# 00_CADRAGE — PERF_MODULE_RESTRUCTURE_PLAN_01

## 1_MASTER_TARGET

Planifier la restructuration physique du cluster PERF, sans deplacer ni modifier le runtime dans ce GO.

## 2_OBJECTIF

```text
Produire :
- la forme cible
- la liste des impacts
- la liste des risques
- le rollback plan
- le GO d'implementation suivant
```

## 3_INCLUS / EXCLUS

```text
INCLUS : target shape, impacts, rollback, gate de decision.
EXCLUS : deplacement de fichiers, changements imports, uvicorn, SQLite, desk_pro, webhook, runtime.
```

## 12_INVARIANTS

```text
- docs only
- 0 migration executee
- 0 changement uvicorn
- 0 changement SQLite path
- 0 changement imports
- 0 secret
```
