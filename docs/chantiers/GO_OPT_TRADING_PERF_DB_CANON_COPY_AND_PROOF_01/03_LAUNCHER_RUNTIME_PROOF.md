---
doc_id: GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01_LAUNCHER_RUNTIME_PROOF
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
  - launchers
  - proof
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/03_LAUNCHER_RUNTIME_PROOF.md
point_de_reprise: "Prouver G3: launchers PERF utilisent le chemin canonique."
updated_at: 2026-05-11
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_DB_CANON_COPY_AND_PROOF_01/00_CADRAGE.md
---

# 03_LAUNCHER_RUNTIME_PROOF

## G3 — Launchers PERF sont canon-ready

Preuves collectées sur `/opt/trading` :

```text
scripts/desk_pro_ui_toolbox_fix_cmd.sh
  → PERF_DB_PATH="$(resolve_perf_db_path)" nohup ... uvicorn modules.perf.app:app ...

scripts/desk_pro_ui_toolbox_final_cmd.sh
  → PERF_DB_PATH="$(resolve_perf_db_path)" nohup ... uvicorn modules.perf.app:app ...

modules/simex_bitget_bridge/cmd.sh
  → PERF_DB_PATH="$(resolve_perf_db_path)" nohup ... uvicorn modules.perf.app:app ...
```

Résolveur `resolve_perf_db_path` dans chaque launcher :

```text
1. PERF_DB_PATH si déjà exporté
2. modules/perf/data/perf.db si présent
3. fallback perf/perf.db
```

La DB canonique étant maintenant présente, le résolveur la préférera automatiquement au fallback legacy.

Verdict G3 :

```text
PROUVÉ
```
