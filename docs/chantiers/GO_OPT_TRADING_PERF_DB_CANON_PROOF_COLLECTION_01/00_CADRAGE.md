---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01
topic_keys:
  - opt-trading
  - perf
  - db
  - proof
  - audit
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/00_CADRAGE.md
point_de_reprise: "Collecter les preuves manquantes avant tout retrait de perf/perf.db."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/01_GATE_CONDITIONS.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/02_RETIRE_DECISION.md
---

# 00_CADRAGE — GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01

## 1_MASTER_TARGET

Collecter les preuves nécessaires pour statuer sur G1, G3 et G4 avant toute exécution de `GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01`.

## 2_RÈGLES

```text
- audit/proof only
- read-only autant que possible
- aucun déplacement DB
- aucune modification launcher/service
- aucune simulation de preuve
```

## 3_GATES A PROUVER

```text
G1. existence réelle de la DB canonique
G2. état du legacy perf/perf.db (constat complémentaire)
G3. preuve que les launchers utilisent réellement la DB canonique
G4. preuve d'absence d'écritures résiduelles sur perf/perf.db
```

## RISKS

- À qualifier.
