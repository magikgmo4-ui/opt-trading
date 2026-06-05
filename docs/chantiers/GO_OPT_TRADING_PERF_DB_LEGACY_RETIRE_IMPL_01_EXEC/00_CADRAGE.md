---
doc_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC
status: final
lifecycle_stage: closeout
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01
topic_keys:
  - opt-trading
  - perf
  - db
  - legacy-retire
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_IMPL_01_EXEC/00_CADRAGE.md
point_de_reprise: "Ajouter retire/unretire au script de relocation PERF et exécuter le retrait du legacy sur /opt/trading."
updated_at: 2026-05-12
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/90_CLOSEOUT.md
---

# 00_CADRAGE — PERF_DB_LEGACY_RETIRE_IMPL_01

## 1_MASTER_TARGET

Implémenter et exécuter le retrait non destructif de la DB legacy `perf/perf.db` sur `/opt/trading`, une fois la DB canonique validée.

## 2_IMPLEMENTATION

```text
perf_db_relocate.sh :
  + retire  : renomme legacy → .retired_TIMESTAMP (exige canonical présent)
  + unretire : restaure le plus récent .retired_* vers le chemin legacy

modules/perf/README.md :
  + documentation des commandes retire/unretire
```

## 3_EXECUTION SUR /opt/trading

```text
LEGACY_DB=/opt/trading/perf/perf.db
CANONICAL_DB=/opt/trading/modules/perf/data/perf.db

retire → legacy renamed to perf/perf.db.retired_20260512_000848
legacy_exists=0, canonical_exists=1
```

## RISKS

- À qualifier.
