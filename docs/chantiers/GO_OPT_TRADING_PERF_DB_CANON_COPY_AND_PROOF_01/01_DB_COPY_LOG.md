---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01_DB_COPY_LOG
doc_type: execution_log
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
  - copy-log
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/01_DB_COPY_LOG.md
point_de_reprise: "Exécution de la copie non destructive de la DB PERF."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/00_CADRAGE.md
---

# 01_DB_COPY_LOG

## PRECHECK

```text
branch        : go/PERF-RUNTIME-SYNC-20260511_232938
ahead/behind  : 0/0 vs origin/sot/mainline
legacy_db     : present, 36864 bytes
canonical_dir : present, empty (README.md only)
script        : perf_db_relocate.sh, copy_db() uses cp -a
```

## COPY EXECUTION

```text
commande : bash modules/perf/scripts/perf_db_relocate.sh copy
methode  : cp -a (copie preservant les attributs)
```

## VERIFICATION

```text
legacy_db:
  path  : /opt/trading/perf/perf.db
  size  : 36864
  mtime : 2026-04-09 11:55:46 -0400
  md5   : e2a92f3aa630fde1e59fb4ef88b5666c

canonical_db:
  path  : /opt/trading/modules/perf/data/perf.db
  size  : 36864
  mtime : 2026-04-09 11:55:46 -0400 (identiques)
  md5   : e2a92f3aa630fde1e59fb4ef88b5666c (identiques)
```

```text
La copie est strictement non destructive.
Le legacy est intact.
Le checksum est identique.
```

## RISKS

- À qualifier.
