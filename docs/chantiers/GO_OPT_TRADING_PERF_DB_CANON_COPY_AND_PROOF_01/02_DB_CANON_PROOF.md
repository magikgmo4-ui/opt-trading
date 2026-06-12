---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01_DB_CANON_PROOF
doc_type: proof_report
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_IMPL_01
topic_keys:
  - opt-trading
  - perf
  - db
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/02_DB_CANON_PROOF.md
point_de_reprise: "Prouver G1: existence et intégrité de la DB canonique."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/01_DB_COPY_LOG.md
---

# 02_DB_CANON_PROOF

## G1 — DB canonique réelle

```text
Preuve :
  path   = /opt/trading/modules/perf/data/perf.db
  size   = 36864
  md5    = e2a92f3aa630fde1e59fb4ef88b5666c
  legacy = intact, identique
  backup = backup/pre-perf-sync-20260511_232839
```

Verdict G1 :

```text
PROUVÉ
```

## G2 — État de la DB legacy

```text
La DB legacy existe encore et est préservée.
Elle ne sera pas retirée dans ce GO.
```

## RISKS

- À qualifier.
