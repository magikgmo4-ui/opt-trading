---
doc_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01_INVENTORY
doc_type: cluster_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_inventory
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - perf
  - inventory
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/01_PERF_CLUSTER_INVENTORY.md
point_de_reprise: "Inventaire complet des 4 composants PERF, imports, data flow, orchestration."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_PERF_CLUSTER_01/00_CADRAGE.md
---

# 01_PERF_CLUSTER_INVENTORY

## 1_PERF_ENGINE — modules/perf_engine/

```text
Fichiers  : 7 (dont 2 configs JSON, 3 scripts shell)
Rôle      : Moteur de performance CLI standalone
Atlas     : KEEP_CANDIDATE (preuves live, USABLE_LIMITED potentiel)

app/perf_engine.py (233 lignes) :
  - Classe PerfEngine : charge positions + executions JSON
  - Rule engine : mappe (position_status, execution_status) → perf_state
  - États : TRACKING, AWAITING_MARK_TO_MARKET, WATCHLIST, REVIEW, BLOCKED, INACTIVE
  - CLI : status, sample, track, export, explain
  - Sortie : data/perf/perf_engine.json

config/sample_positions.json : 3 entrées (BTCUSDT, ETHUSDT, SOLUSDT)
config/sample_execution.json : 3 entrées (READY, BLOCKED, READY)
scripts/ : cmd.sh, menu.sh, sanity_check.sh

Imports Python : stdlib uniquement (sys, os, json, argparse, datetime, pathlib)
Consommé par :
  - desk_pro_orchestrator (subprocess : python -m modules.perf_engine.app.perf_engine)
  - desk_pro_dashboard (lit perf_engine.json)
  - scripts/desk_pro_copy_latest_to_shared.sh (copie l'artefact JSON)
```

## 2_PERF_FACADE — modules/perf/

```text
Fichiers  : 5 (4 scripts shell + README)
Rôle      : Façade shell mince pour la surface Perf
Atlas     : dans le cluster PERF, pas un produit Atlas séparé

README.md : "The main app remains perf/perf_app.py. This facade serves mainly
            to expose the Perf surface uniformly for operators."
            "Do not duplicate logic from perf/perf_app.py here."

scripts/ :
  - cmd.sh : wrapper générique (info, readme, ls, grep, menu)
  - menu.sh : menu interactif (README, ls, grep, git status)
  - sanity_check.sh : validation structure
  - install_shortcuts.sh : liens /usr/local/bin/menu-perf, cmd-perf

Aucun code Python. Shell uniquement.
Pointe vers perf/perf_app.py (le vrai runtime).
```

## 3_PERF_APP — perf/perf_app.py

```text
Fichier   : 1 (995 lignes, racine du repo)
Rôle      : Serveur FastAPI + SQLite, runtime PERF actif
Atlas     : dans le cluster PERF

Architecture :
  - Base SQLite : perf/perf.db (WAL mode, tables events et trades)
  - API :
    POST /perf/event      → ingest OPEN/CLOSE/UPDATE
    GET  /perf/summary    → KPIs (PnL, winrate, drawdown)
    GET  /perf/equity     → courbe equity
    GET  /perf/open       → positions ouvertes
    GET  /perf/trades     → historique (filtres engine, symbol, status)
    GET  /perf/ui         → dashboard HTML (Perf Control Center)
  - Desk Pro : monté sur /desk (via modules.desk_pro)
  - Moniteurs : alertes Telegram (no-activity 30min, drawdown 5%/7%)
  - Runtime : uvicorn perf.perf_app:app --port 8010

Imports :
  - modules.env.env
  - modules.desk_pro.api.routes
  - modules.desk_pro.mount
  - shared.logger
  - fastapi, pydantic

Dépendances critiques :
  - modules/desk_pro/ (ne pas casser)
  - perf/perf.db (ne pas déplacer sans maj config)
  - uvicorn path perf.perf_app:app (ne pas changer sans maj scripts)
```

## 4_WEBHOOK_ADAPTER — adapters/webhook_to_perf.py

```text
Fichier   : 1 (121 lignes, dans adapters/)
Rôle      : Convertit les payloads webhook en PerfEvent (POST /perf/event)
Atlas     : dans le cluster PERF

Fonctions :
  - webhook_event_to_perf_event(evt) : convertisseur principal
    - Normalise event_type (OPEN/CLOSE/UPDATE, filtre SIGNAL)
    - Normalise side (BUY→LONG, SELL→SHORT)
    - Filtre engines de test (TV_TEST, _TEST_*, TEST_*)
    - Valide champs obligatoires par type
    - Génère trade_id si absent
  - build_trade_id(engine, symbol, side, payload) : T_ts_engine_symbol_side_hash

Imports : hashlib, json, datetime, typing (stdlib uniquement)
Callers  : AUCUN caller trouvé dans le repo
Statut   : Code prêt, non intégré dans le pipeline actif
```

## 5_CROSS_REFERENCES

### Imports Python directs

```text
AUCUN import croisé entre les 4 composants PERF.
  perf_engine       → stdlib uniquement
  modules/perf/     → pas de code Python
  perf/perf_app.py  → modules.desk_pro.*, modules.env, shared.logger
  webhook_to_perf   → stdlib uniquement
```

### Data flow

```text
[perf_engine] ──perf_engine.json──> [desk_pro_orchestrator]
                                   ──perf_engine.json──> [desk_pro_dashboard]
[webhook] ──POST /perf/event─────> [perf/perf_app.py :8010]
```

### Orchestration (shell)

```text
scripts/simex_bitget_bridge/cmd.sh          → uvicorn perf.perf_app:app --port 8010
scripts/desk_pro_ui_toolbox_final_cmd.sh    → kill/restart perf_app
scripts/desk_pro_ui_toolbox_fix_cmd.sh      → kill/restart perf_app
scripts/desk_pro_copy_latest_to_shared.sh   → cp perf_engine.json
scripts/verify_all.sh                       → compile perf/perf_app.py + webhook_to_perf.py
```

### Registry

```text
registry/ui_surfaces_registry.yaml → enregistre perf_engine, perf_app
```

## 6_FICHIERS_ORPHELINS_DETECTES

```text
adapters/webhook_to_perf.py :
  - Aucun caller trouvé dans le repo
  - Fonctionnel mais non intégré
  - À intégrer ou archiver (décision dans un GO séparé)

perf/perf.db :
  - Base SQLite active, utilisée par perf_app en runtime
  - Chemin hardcodé dans perf_app.py
  - Ne pas déplacer sans GO dédié
```

## 7_RESUME

```text
4 composants PERF, zéro import Python croisé.
2 flux de données : JSON (perf_engine) + HTTP (perf_app).
1 composant orphelin : webhook_to_perf.py (aucun caller).
3 dépendances externes : desk_pro (API mount), uvicorn runtime, SQLite.
Toute restructuration toucherait desk_pro, uvicorn, SQLite — GO séparé obligatoire.
```

## RISKS

- À qualifier.
