---
doc_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01_GATES_AND_ROLLBACK
doc_type: gates_and_rollback
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01
status: draft_for_review
lifecycle_stage: child_gates
parent_go_id: GO_OPT_TRADING_PERF_PATH_SWITCH_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - rollback
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01/03_GATES_AND_ROLLBACK.md
point_de_reprise: "Fixer les gates avant toute relocation de perf.db."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_RELOCATION_PLAN_01/02_TARGET_RELOCATION_PLAN.md
---

# 03_GATES_AND_ROLLBACK

## 1_GATES

```text
G1. backup vérifié de perf/perf.db
G2. preuve que PERF_DB_PATH override est bien pris en compte dans l'environnement réel
G3. test de création/lecture sur DB candidate sans perte
G4. vérification des endpoints /perf/* et /desk/* après switch en staging
G5. rollback testé sur papier et scripts listés
```

## 2_ROLLBACK

```text
Rollback minimal :
- remettre PERF_DB_PATH vers perf/perf.db
- restaurer la copie backup si écriture partielle problématique
- relancer le service PERF sur l'ancien chemin
```

## 3_NEXT_GO

```text
GO_OPT_TRADING_PERF_DB_RELOCATION_IMPL_01
```

## RISKS

- À qualifier.
