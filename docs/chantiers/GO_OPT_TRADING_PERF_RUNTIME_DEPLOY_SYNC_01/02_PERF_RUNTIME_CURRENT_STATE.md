---
doc_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01_PERF_RUNTIME_CURRENT_STATE
doc_type: runtime_state
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01
status: draft_for_review
lifecycle_stage: child_runtime_state
parent_go_id: GO_OPT_TRADING_PERF_DB_CANON_RUNTIME_PROOF_01
topic_keys:
  - opt-trading
  - perf
  - runtime
  - current-state
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/02_PERF_RUNTIME_CURRENT_STATE.md
point_de_reprise: "Documenter l'état PERF réellement observé sur /opt/trading."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PERF_RUNTIME_DEPLOY_SYNC_01/00_CADRAGE.md
---

# 02_PERF_RUNTIME_CURRENT_STATE

## 1_DB PATHS OBSERVÉS

```text
/opt/trading/modules/perf/data/         = absent
/opt/trading/modules/perf/data/perf.db  = absent

/opt/trading/perf/perf.db               = present
size                                    = 36864
mtime                                   = 2026-04-09 11:55:46 -0400
```

## 2_LAUNCHERS OBSERVÉS SUR /opt/trading

```text
scripts/desk_pro_ui_toolbox_fix_cmd.sh   -> uvicorn perf.perf_app:app
scripts/desk_pro_ui_toolbox_final_cmd.sh -> uvicorn perf.perf_app:app
modules/simex_bitget_bridge/cmd.sh       -> uvicorn perf.perf_app:app
```

## 3_PROCESS / SERVICE STATE OBSERVÉE

```text
listener :8010   -> none observed
uvicorn perf     -> none observed
systemd perf     -> none observed explicitly during audit
```

## 4_LECTURE CORRECTE

```text
Le runtime réel observé sur /opt/trading ne montre pas :
- de DB canonique
- de launcher canonique actif
- de process PERF actif au moment de la collecte

Il montre encore :
- un code launcher historique orienté legacy
- une DB legacy présente
```
