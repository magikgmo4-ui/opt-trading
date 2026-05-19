---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01_LEGACY_WRITE_ABSENCE_PROOF
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
  - legacy
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/03_LEGACY_WRITE_ABSENCE_PROOF.md
point_de_reprise: "Prouver ou refuser de prouver l'absence d'écritures sur perf/perf.db."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/00_CADRAGE.md
---

# 03_LEGACY_WRITE_ABSENCE_PROOF

## G4 — Aucune écriture résiduelle sur `perf/perf.db` ?

Preuves disponibles dans ce worktree :

```text
legacy_mtime=missing
legacy_size=missing
```

Mais :

```text
L'absence de `perf/perf.db` dans ce worktree n'est PAS une preuve suffisante
de l'absence d'écritures sur l'environnement runtime réel.

Il manque :
- logs de démarrage réels avec PERF_DB_PATH canonique
- observation d'écriture effective sur la DB canonique
- observation d'absence d'écriture sur la DB legacy réelle
```

Verdict G4 :

```text
NON PROUVÉ
```

## Résumé opérationnel

```text
Le repo est prêt pour la bascule canonique,
mais la preuve runtime réelle n'est pas collectée dans ce lot read-only.
```
