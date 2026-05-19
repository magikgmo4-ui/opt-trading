---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01_LAUNCHER_RUNTIME_PROOF
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
  - launchers
  - runtime-proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/02_LAUNCHER_RUNTIME_PROOF.md
point_de_reprise: "Prouver le chemin réellement utilisé par les launchers sur /opt/trading."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01/00_CADRAGE.md
---

# 02_LAUNCHER_RUNTIME_PROOF

## G3 — Launchers/services pointent-ils réellement vers la DB canonique ?

Preuves runtime réelles lues dans `/opt/trading` :

```text
scripts/desk_pro_ui_toolbox_fix_cmd.sh
  -> uvicorn perf.perf_app:app

scripts/desk_pro_ui_toolbox_final_cmd.sh
  -> uvicorn perf.perf_app:app

modules/simex_bitget_bridge/cmd.sh
  -> uvicorn perf.perf_app:app
```

Autre preuve critique :

```text
/opt/trading est sur la branche : go/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
et derrière origin/sot/mainline de 226 commits.
```

Lecture correcte :

```text
La surface runtime réelle /opt/trading n'embarque pas encore les launchers canon-ready
introduits plus tard dans sot/mainline.

Donc, même si le repo documentaire/canonique sait résoudre PERF_DB_PATH,
la surface runtime réelle observée ici n'utilise pas encore ces scripts.
```

Preuve d'exécution active :

```text
aucun listener sur :8010 observé
aucun service PERF explicite observé
```

Verdict G3 :

```text
NON PROUVÉ
```
