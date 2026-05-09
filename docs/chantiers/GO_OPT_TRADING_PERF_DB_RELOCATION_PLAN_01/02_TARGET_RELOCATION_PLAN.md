---
doc_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01_TARGET_RELOCATION_PLAN
doc_type: relocation_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_relocation_plan
parent_go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - relocation-plan
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01/02_TARGET_RELOCATION_PLAN.md
point_de_reprise: "Définir la cible de relocation de perf.db et la séquence future."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01/01_CURRENT_DB_STATE.md
---

# 02_TARGET_RELOCATION_PLAN

## 1_TARGET CANDIDATE

```text
Target candidate path:
  modules/perf/data/perf.db

Reason:
  - rapproche la DB de la surface canonique modules/perf/
  - sépare mieux code historique perf/ et surface canonique
  - prépare une future clarification de la boundary PERF
```

## 2_SEQUENCING FUTURE

```text
1. backup complet de perf/perf.db
2. test de lecture sur copie
3. introduction d'un PERF_DB_PATH explicite dans les environnements cibles
4. run en staging sur nouveau chemin
5. vérification /perf/ui + /desk + writes
6. bascule contrôlée
7. période de coexistence surveillée
```

## 3_NON GOALS

```text
- ne pas déplacer physiquement la DB ici
- ne pas supprimer perf/perf.db ici
- ne pas changer l'initialisation sqlite ici
```
