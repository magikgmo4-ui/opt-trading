---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01_DB_CANON_PROOF
doc_type: proof_report
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01
status: draft_for_review
lifecycle_stage: child_proof_report
parent_go_id: GO_OPT_TRADING_PERF_DB_LEGACY_RETIRE_GATE_01
topic_keys:
  - opt-trading
  - perf
  - db
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/01_DB_CANON_PROOF.md
point_de_reprise: "Prouver l'existence réelle de la DB canonique et constater l'état du legacy."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/00_CADRAGE.md
---

# 01_DB_CANON_PROOF

## G1 — DB canonique réelle

Preuve collectée dans le repo/worktree :

```text
modules/perf/data/
  - README.md seulement
  - aucun fichier perf.db présent
```

Constat brut :

```text
CANON_DB_FILE
missing

CANON_DB_DIR
total 12K
drwxr-xr-x ... modules/perf/data/
-rw-r--r-- README.md
```

Verdict G1 :

```text
NON PROUVÉ
```

## G2 — État du legacy `perf/perf.db`

Preuve collectée dans le repo/worktree :

```text
LEGACY_DB_FILE
missing

LEGACY_GREP
not_tracked
```

Lecture correcte :

```text
Le snapshot repo/worktree ne contient ni la DB legacy, ni la DB canonique.
Cela ne prouve PAS qu'elles sont absentes de l'environnement runtime réel /opt/trading.
Cela prouve seulement qu'elles ne sont pas présentes dans ce worktree et non suivies par git.
```

Verdict G2 :

```text
CONSTAT PARTIEL UNIQUEMENT
```
