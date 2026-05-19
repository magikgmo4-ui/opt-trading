---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
status: draft_for_review
lifecycle_stage: child_cadrage
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01
topic_keys:
  - opt-trading
  - perf
  - db
  - runtime-proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/00_CADRAGE.md
point_de_reprise: "Collecter les preuves runtime réelles manquantes sur /opt/trading avant tout retrait legacy PERF DB."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01/01_GATE_CONDITIONS.md
---

# 00_CADRAGE — GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01

## 1_MASTER_TARGET

Prouver ou refuser de prouver, sur la surface runtime réelle `/opt/trading`, les gates G1, G3 et G4 avant tout retrait de `perf/perf.db`.

## 2_RÈGLES

```text
- audit/preuve only
- read-only autant que possible
- aucune mutation runtime
- aucune création artificielle de DB canonique
- aucun restart service
```
