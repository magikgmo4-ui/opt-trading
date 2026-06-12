---
doc_id: GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01
topic_keys:
  - opt-trading
  - perf
  - db
  - relocation
  - implementation
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01/00_CADRAGE.md
point_de_reprise: "Implémenter l’outillage de relocation DB sans changer le runtime par défaut."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01/90_CLOSEOUT.md
---

# 00_CADRAGE — GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01

## 1_MASTER_TARGET

Implémenter un outillage de relocation DB non destructif pour PERF, sans basculer automatiquement le runtime.

## 2_CHOIX RETENU

```text
- créer le chemin canonique candidat `modules/perf/data/`
- fournir un script status/copy/show-env
- laisser le runtime historique inchangé tant que PERF_DB_PATH n'est pas posé
```

## RISKS

- À qualifier.
