---
doc_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01_SWITCH_GATES
doc_type: switch_gates
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01
status: draft_for_review
lifecycle_stage: child_switch_gates
parent_go_id: GO_OPT_TRADING_PERF_MODULE_RESTRUCTURE_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - gates
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/02_SWITCH_GATES.md
point_de_reprise: "Definir les gates avant basculement des chemins PERF."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_PATH_SWITCH_PLAN_01/01_SWITCH_MATRIX.md
---

# 02_SWITCH_GATES

## 1_GATES

```text
G1. FastAPI dependencies disponibles dans l'environnement de validation
G2. test d'import `modules.perf.app:app` valide dans l'environnement reel
G3. tous les scripts de lancement mis a jour dans une branche de test
G4. verification que /perf/ui et /desk montent encore
G5. rollback shell simple prete
```

## 2_NON GOALS

```text
- ne pas deplacer perf.db ici
- ne pas retirer les anciens chemins ici
- ne pas reconfigurer uvicorn ici
```

## RISKS

- À qualifier.
