---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01_LAUNCHER_PATH_PROOF
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
  - launchers
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/02_LAUNCHER_PATH_PROOF.md
point_de_reprise: "Prouver ou refuser de prouver que les launchers utilisent réellement la DB canonique."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_PROOF_COLLECTION_01/00_CADRAGE.md
---

# 02_LAUNCHER_PATH_PROOF

## G3 — Launchers utilisent réellement la DB canonique ?

Preuves de code collectées :

```text
perf/perf_app.py:19
  DB_PATH = os.getenv("PERF_DB_PATH", os.path.join(APP_DIR, "perf.db"))

modules/perf/README.md:53-55
  1. PERF_DB_PATH si deja exporte
  2. modules/perf/data/perf.db si ce fichier existe
  3. fallback legacy perf/perf.db

scripts/desk_pro_ui_toolbox_fix_cmd.sh
scripts/desk_pro_ui_toolbox_final_cmd.sh
modules/simex_bitget_bridge/cmd.sh
  resolvent PERF_DB_PATH dans cet ordre :
  - PERF_DB_PATH explicite
  - DB canonique si presente
  - fallback legacy sinon
```

Conclusion rigoureuse :

```text
Le CODE est prêt à utiliser la DB canonique.
Mais aucune preuve runtime n'établit qu'il l'utilise effectivement aujourd'hui.
Comme la DB canonique est absente dans le worktree, le comportement effectif
de ces launchers ici serait un fallback vers perf/perf.db.
```

Verdict G3 :

```text
NON PROUVÉ
```

## RISKS

- À qualifier.
