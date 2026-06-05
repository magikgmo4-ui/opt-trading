---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01_RUNTIME_DB_RESOLUTION_PROOF
doc_type: proof_report
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
status: draft_for_review
lifecycle_stage: child_proof_report
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01
topic_keys:
  - opt-trading
  - perf
  - db
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/01_RUNTIME_DB_RESOLUTION_PROOF.md
point_de_reprise: "Prouver l'état réel de la DB canonique et legacy sur /opt/trading."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/00_CADRAGE.md
---

# 01_RUNTIME_DB_RESOLUTION_PROOF

## G1 — DB canonique réelle sur `/opt/trading`

Preuves runtime réelles :

```text
/opt/trading -> /home/fantome/opt-trading

/opt/trading/modules/perf/data
  missing
```

Constat :

```text
La surface runtime réelle /opt/trading ne contient pas de dossier canonique exploitable,
et donc aucune `modules/perf/data/perf.db` n'est présente.
```

Verdict G1 :

```text
NON PROUVÉ
```

## Legacy DB réelle

Preuves runtime réelles :

```text
/opt/trading/perf/perf.db
  taille = 36864
  modif  = 2026-04-09 11:55:46 -0400
```

Constat :

```text
La DB legacy existe réellement sur la surface runtime.
```

## RISKS

- À qualifier.
