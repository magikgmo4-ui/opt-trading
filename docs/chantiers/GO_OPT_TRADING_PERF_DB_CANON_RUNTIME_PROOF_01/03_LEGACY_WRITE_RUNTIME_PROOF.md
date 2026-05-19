---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01_LEGACY_WRITE_RUNTIME_PROOF
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
  - legacy
  - runtime-proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/03_LEGACY_WRITE_RUNTIME_PROOF.md
point_de_reprise: "Prouver ou refuser de prouver l'absence d'écritures sur perf/perf.db côté runtime réel."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/00_CADRAGE.md
---

# 03_LEGACY_WRITE_RUNTIME_PROOF

## G4 — Absence d’écritures résiduelles sur `perf/perf.db`

Preuves runtime réelles :

```text
legacy db présente
mtime = 2026-04-09 11:55:46 -0400
taille = 36864

aucun listener :8010 observé pendant la collecte
aucun service PERF explicite observé pendant la collecte
```

Mais :

```text
L'absence de processus PERF au moment T n'est pas une preuve suffisante
de l'absence d'écritures résiduelles sur la durée.

Il manque :
- une fenêtre d'observation runtime réelle
- logs de démarrage montrant la DB effectivement utilisée
- preuve qu'aucune automation ne réactive encore perf/perf.db
```

Verdict G4 :

```text
NON PROUVÉ
```
