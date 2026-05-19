---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_LOCALCMS_MENU
doc_type: ui_impl_plan
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 11_LOCALCMS_MENU_DISPLAY_PLAN

## Objet

Plan parallèle pour afficher le menu global OPT-TRADING dans LocalCMS.
LocalCMS devient le cockpit de navigation du système — pas un dashboard opérationnel (c'est Desk Pro),
mais une carte vivante de l'architecture.

---

## PRINCIPE FONDAMENTAL

```text
LocalCMS MENU = navigation dans les 14 domaines du système opt-trading
Chaque item de menu = une vue de l'état actuel du module/domaine
Source de données = fichier menu JSON (statique) + health endpoints (dynamique)
Refresh = polling léger côté client (30s pour états, 5min pour structurel)

CE N'EST PAS un dashboard temps réel.
C'EST une carte d'architecture vivante avec états.
```

---

## ARCHITECTURE DU MENU LOCALCMS

### Couche 1 — Registry JSON (source structurelle)

```text
FICHIER: scripts/ai/menu/opt_trading_menu.json
RÔLE: définit la structure complète du menu (14 domaines + sous-menus)
ALIMENTATION: statique (mis à jour lors des GO)
FORMAT:
{
  "menu": [
    {
      "id": "pipeline_trading",
      "label": "Pipeline Trading",
      "icon": "chart-line",
      "children": [...]
    }
  ]
}

SOURCE ADDITIONNELLE:
ui_registry_msi/config/ → registry des surfaces UI → enrichit automatiquement le menu
```

### Couche 2 — État dynamique (health polling)

```text
FICHIER: scripts/ai/menu/menu_state_aggregator.sh
RÔLE: interroge les health endpoints de chaque module opérationnel
OUTPUT: scripts/ai/menu/state_cache.json (refresh toutes les 30s)
FORMAT:
{
  "gateway_openclaw": {"status": "live", "last_check": "2026-05-16T10:00:00Z"},
  "desk_pro": {"status": "live", "last_check": "..."},
  ...
}
```

### Couche 3 — LocalCMS consumer (rendu)

```text
LocalCMS lit:
  1. opt_trading_menu.json      → structure navigation
  2. state_cache.json           → états modules
  3. ui_registry_msi/config/   → surfaces UI disponibles (enrichissement)

LocalCMS affiche:
  → menu latéral 14 domaines
  → indicateur état par module (•OUI / ○IMPL / ⊘SPEC / ✕CLOSED)
  → vue détail par module (clic)
  → vue détail par domaine (liste modules + états)
```

---

## STRUCTURE JSON DU MENU

```json
{
  "version": "1.0",
  "updated_at": "2026-05-16",
  "menu": [
    {
      "id": "1_pipeline_trading",
      "label": "Pipeline Trading",
      "icon": "⚡",
      "children": [
        {
          "id": "1_1_signal",
          "label": "Signal & Webhook",
          "children": [
            {"id": "tradingview_observer", "label": "TradingView Observer", "status": "operational", "machine": "admin-trading"},
            {"id": "tradingview_observer_openclaw", "label": "TV Observer OpenClaw", "status": "impl", "machine": "admin-trading"},
            {"id": "webhook", "label": "Webhook Handler", "status": "impl", "machine": "admin-trading"}
          ]
        },
        {
          "id": "1_2_decision",
          "label": "Décision & Ranking",
          "children": [
            {"id": "decision_engine", "label": "Decision Engine", "status": "impl", "machine": "admin-trading"},
            {"id": "opportunity_ranker", "label": "Opportunity Ranker", "status": "impl", "machine": "admin-trading"},
            {"id": "probability_engine", "label": "Probability Engine", "status": "impl", "machine": "admin-trading"}
          ]
        },
        {
          "id": "1_3_risk",
          "label": "Risque & Kill Switch",
          "children": [
            {"id": "risk_engine", "label": "Risk Engine", "status": "impl", "machine": "admin-trading"},
            {"id": "kil_v1", "label": "Kill Switch (kil_v1)", "status": "operational", "machine": "admin-trading"}
          ]
        },
        {
          "id": "1_4_execution",
          "label": "Exécution & Exchange",
          "children": [
            {"id": "execution_engine", "label": "Execution Engine", "status": "impl", "machine": "admin-trading"},
            {"id": "simex_bitget_bridge", "label": "SimEx Bitget Bridge", "status": "operational", "machine": "admin-trading"}
          ]
        },
        {
          "id": "1_5_position",
          "label": "Position & Portfolio",
          "children": [
            {"id": "position_engine", "label": "Position Engine", "status": "impl", "machine": "admin-trading"},
            {"id": "portfolio_engine", "label": "Portfolio Engine", "status": "impl", "machine": "admin-trading"}
          ]
        },
        {
          "id": "1_6_observation",
          "label": "Observation & Lab",
          "children": [
            {"id": "trading_realtime_v1", "label": "Trading Realtime V1", "status": "impl", "machine": "admin-trading"},
            {"id": "trading_lab_v1", "label": "Trading Lab V1", "status": "impl", "machine": "admin-trading"}
          ]
        }
      ]
    },
    {
      "id": "2_market_data",
      "label": "Market Data",
      "icon": "📊",
      "children": [
        {"id": "2_1_collectors", "label": "Collectors", "children": [
          {"id": "collector_binance_spot", "label": "Binance Spot", "status": "partial"},
          {"id": "collector_coingecko", "label": "CoinGecko", "status": "partial"},
          {"id": "derivatives_collector", "label": "Derivatives Collector", "status": "impl"}
        ]},
        {"id": "2_2_analyzers", "label": "Analyseurs", "children": [
          {"id": "derivatives_analyzer", "label": "Derivatives Analyzer", "status": "impl"},
          {"id": "liquidation_analyzer", "label": "Liquidation Analyzer", "status": "impl"}
        ]},
        {"id": "2_3_hub", "label": "Hub & Scanner", "children": [
          {"id": "market_scanner", "label": "Market Scanner", "status": "impl"},
          {"id": "marketdata", "label": "MarketData Hub", "status": "impl"}
        ]}
      ]
    },
    {
      "id": "3_openclaw",
      "label": "OpenClaw Runtime",
      "icon": "🤖",
      "children": [
        {"id": "3_1_gateway", "label": "Gateway & Bridge", "children": [
          {"id": "gateway_openclaw", "label": "Gateway OpenClaw", "status": "operational", "health_url": "ws://127.0.0.1:18789/health"},
          {"id": "openclaw_operator_bridge", "label": "Operator Bridge", "status": "to_build", "priority": 1}
        ]},
        {"id": "3_2_config", "label": "Configuration & Diagnostic", "children": [
          {"id": "configure_openclaw", "label": "Configure", "status": "operational"},
          {"id": "openclaw_config_modulaire", "label": "Config Modulaire", "status": "operational"},
          {"id": "doctor_openclaw", "label": "Doctor", "status": "operational"},
          {"id": "evidence_openclaw", "label": "Evidence", "status": "operational"}
        ]},
        {"id": "3_3_install", "label": "Installation & Providers", "children": [
          {"id": "install_module_openclaw", "label": "Install Module", "status": "operational"},
          {"id": "model_provider_openclaw", "label": "Model Provider", "status": "operational"}
        ]},
        {"id": "3_4_interface", "label": "Interface & Bridge", "children": [
          {"id": "menu_openclaw", "label": "Menu OpenClaw", "status": "operational"},
          {"id": "tradingview_observer_openclaw", "label": "TV Observer Bridge", "status": "impl"}
        ]}
      ]
    },
    {
      "id": "4_ai_providers",
      "label": "AI & Providers",
      "icon": "🧠",
      "children": [
        {"id": "memory_bricks", "label": "Memory Bricks", "status": "operational"},
        {"id": "validated_prompt_factory", "label": "Prompt Factory", "status": "operational"},
        {"id": "deepseek_hub", "label": "DeepSeek Hub", "status": "impl"},
        {"id": "deepseek_response", "label": "DeepSeek Response", "status": "impl"},
        {"id": "deepseek_thinking", "label": "DeepSeek Thinking", "status": "impl"},
        {"id": "hf_free_platform", "label": "HF Platform", "status": "impl"}
      ]
    },
    {
      "id": "5_desk_pro",
      "label": "Desk Pro — UI Trading",
      "icon": "🖥️",
      "children": [
        {"id": "5_1_entry", "label": "Entrée Opératoire", "children": [
          {"id": "desk_pro_runner", "label": "Desk Runner", "status": "operational"},
          {"id": "desk_pro_orchestrator", "label": "Desk Orchestrator", "status": "operational"}
        ]},
        {"id": "5_2_ui", "label": "UI Centrale", "children": [
          {"id": "desk_pro", "label": "Desk Pro (FastAPI)", "status": "operational"},
          {"id": "desk_pro_dashboard", "label": "Dashboard", "status": "impl"}
        ]},
        {"id": "5_3_pipeline", "label": "Pipeline Snapshot (0→A→B→D→E)", "children": [
          {"id": "desk_retention", "label": "Step 0 — Retention", "status": "operational"},
          {"id": "desk_snapshot_ingest", "label": "Step A — Snapshot Ingest", "status": "operational"},
          {"id": "desk_analyze", "label": "Step B — Analyze", "status": "operational"},
          {"id": "desk_capture_inputs", "label": "Step D — Capture Inputs", "status": "operational"},
          {"id": "desk_state", "label": "Step E — State Final", "status": "operational"}
        ]},
        {"id": "desk_common", "label": "Shared (desk_common)", "status": "operational"}
      ]
    },
    {
      "id": "6_vision",
      "label": "Vision & Capture",
      "icon": "👁️",
      "children": [
        {"id": "bot_vision", "label": "Bot Vision (headless + step1)", "status": "operational"},
        {"id": "bot_vision_step2", "label": "Bot Vision Step2", "status": "impl"},
        {"id": "vision_bot", "label": "Vision Bot (SHAREX)", "status": "impl"}
      ]
    },
    {
      "id": "7_perf_journal",
      "label": "Performance & Journal",
      "icon": "📈",
      "children": [
        {"id": "perf", "label": "Perf (shim → perf_engine)", "status": "operational"},
        {"id": "perf_engine", "label": "Perf Engine", "status": "impl"},
        {"id": "journal_engine", "label": "Journal Engine", "status": "impl"}
      ]
    },
    {
      "id": "8_infra",
      "label": "Infra & Connectivité",
      "icon": "🔌",
      "children": [
        {"id": "8_1_ssh", "label": "SSH & Réseau", "children": [
          {"id": "reseau_ssh", "label": "Réseau SSH (canonique)", "status": "operational"},
          {"id": "reseau_ssh_step1b", "label": "SSH Step1b (deprecated)", "status": "deprecated"}
        ]},
        {"id": "8_2_transfer", "label": "Transfert Fichiers", "children": [
          {"id": "shared_files_sftp", "label": "SFTP", "status": "impl"},
          {"id": "shared_sshfs_permanent", "label": "SSHFS Permanent", "status": "impl"},
          {"id": "shared", "label": "Shared Data", "status": "impl"},
          {"id": "winscp_transfer", "label": "WinSCP Transfer", "status": "impl"}
        ]},
        {"id": "8_3_auth", "label": "Auth & Secrets", "children": [
          {"id": "auth", "label": "Auth (credentials)", "status": "operational"}
        ]},
        {"id": "health", "label": "Health Checker", "status": "operational"}
      ]
    },
    {
      "id": "9_registres",
      "label": "Registres & Routage",
      "icon": "🗂️",
      "children": [
        {"id": "ui_registry_msi", "label": "UI Registry MSI", "status": "impl", "note": "source vérité UI"},
        {"id": "registry_router", "label": "Registry Router", "status": "impl"},
        {"id": "registry_meta_reader", "label": "Meta Reader", "status": "impl"},
        {"id": "modules_registry_reader", "label": "Modules Reader", "status": "impl"},
        {"id": "machines_registry_reader", "label": "Machines Reader", "status": "impl"},
        {"id": "wrappers_registry_reader", "label": "Wrappers Reader", "status": "impl"},
        {"id": "router", "label": "Router (facade)", "status": "minimal"}
      ]
    },
    {
      "id": "10_workers",
      "label": "Workers Stricts (À Produire)",
      "icon": "⚙️",
      "children": [
        {"id": "10_1_signal", "label": "Ingestion Signal", "children": [
          {"id": "signal_router", "label": "Signal Router", "status": "to_build", "go": "GO-03"},
          {"id": "notification_dispatcher", "label": "Notification Dispatcher", "status": "to_build", "go": "GO-04"}
        ]},
        {"id": "10_2_ia", "label": "IA Pipeline", "children": [
          {"id": "proposition_engine", "label": "Proposition Engine", "status": "to_build", "go": "GO-06"},
          {"id": "validation_gate", "label": "Validation Gate", "status": "to_build", "go": "GO-07"}
        ]},
        {"id": "10_3_execution", "label": "Exécution & Résultat", "children": [
          {"id": "trade_executor", "label": "Trade Executor", "status": "to_build", "go": "GO-08"},
          {"id": "result_tracker", "label": "Result Tracker", "status": "to_build", "go": "GO-08"}
        ]},
        {"id": "10_4_reporting", "label": "Reporting & Learning", "children": [
          {"id": "datasheet_writer", "label": "Datasheet Writer", "status": "to_build", "go": "GO-09"},
          {"id": "learning_feeder", "label": "Learning Feeder", "status": "to_build", "go": "GO-10"}
        ]},
        {"id": "10_5_sync", "label": "Notifications & Sync", "children": [
          {"id": "task_tracker", "label": "Task Tracker", "status": "to_build"},
          {"id": "ui_renderer", "label": "UI Renderer", "status": "to_build"}
        ]}
      ]
    },
    {
      "id": "11_ops",
      "label": "Ops & Menus",
      "icon": "🔧",
      "children": [
        {"id": "ops_menu_hub", "label": "Ops Menu Hub", "status": "operational"},
        {"id": "ops_super_menu", "label": "Ops Super Menu", "status": "operational"},
        {"id": "ops_wrappers", "label": "Ops Wrappers", "status": "operational"},
        {"id": "module_contextuals_shell", "label": "Module Contextuals Shell", "status": "operational"},
        {"id": "naming_normalizer", "label": "Naming Normalizer", "status": "operational"}
      ]
    },
    {
      "id": "12_tooling",
      "label": "Repo & Tooling",
      "icon": "🛠️",
      "children": [
        {"id": "12_1_validation", "label": "Validation", "children": [
          {"id": "trae_module_validator", "label": "Trae Module Validator", "status": "operational"},
          {"id": "dev_validation_hub", "label": "Dev Validation Hub", "status": "operational"},
          {"id": "audit", "label": "Audit Module", "status": "operational"}
        ]},
        {"id": "12_2_hygiene", "label": "Hygiène & Permissions", "children": [
          {"id": "repo_hygiene", "label": "Repo Hygiene", "status": "operational"},
          {"id": "repo_local_artifacts", "label": "Repo Local Artifacts", "status": "operational"},
          {"id": "repo_ownership_guard", "label": "Ownership Guard", "status": "operational"},
          {"id": "git_fleet_guard", "label": "Git Fleet Guard", "status": "impl"}
        ]},
        {"id": "12_3_sync", "label": "Installation & Sync", "children": [
          {"id": "install_module", "label": "Install Module (sync_validate)", "status": "operational"},
          {"id": "workflow_post_change_v2", "label": "Workflow Post Change V2", "status": "impl"}
        ]}
      ]
    },
    {
      "id": "13_shared_libs",
      "label": "Shared Libs",
      "icon": "📦",
      "children": [
        {"id": "engines", "label": "Engines (registry + router)", "status": "operational"},
        {"id": "env", "label": "Env (bootstrap)", "status": "operational"}
      ]
    },
    {
      "id": "14_archived",
      "label": "Archivés / Fermés",
      "icon": "🗄️",
      "children": [
        {"id": "deepseek_student", "label": "DeepSeek Student", "status": "closed"},
        {"id": "mimo_open_observer", "label": "Mimo Open Observer", "status": "closed"},
        {"id": "perm_fix_student", "label": "Perm Fix Student", "status": "closed"}
      ]
    }
  ]
}
```

---

## PLAN D'IMPLÉMENTATION LOCALCMS — PHASES PARALLÈLES

### PHASE A — Fichiers statiques (immédiat, sans GO pipeline)

```text
TÂCHE A1: Créer opt_trading_menu.json
  FICHIER: scripts/ai/menu/opt_trading_menu.json
  SOURCE: structure JSON ci-dessus
  OWNER: ghost (db-layer)
  TEMPS: 1 session de travail
  PRÉREQ: aucun

TÂCHE A2: Créer state_schema.json
  FICHIER: scripts/ai/menu/state_schema.json
  CONTENU: liste modules healthcheckables + endpoint + machine
  SOURCE: 05_OPERATIONAL_RUNTIME_PLAN.md

TÂCHE A3: Créer menu_state_aggregator.sh
  FICHIER: scripts/ai/menu/menu_state_aggregator.sh
  LOGIQUE:
    → lit state_schema.json
    → pour chaque module avec health endpoint: curl/nc check
    → écrit state_cache.json
    → exécuté toutes les 30s via cron ou boucle tmux
```

### PHASE B — LocalCMS consumer (lecture JSON + rendu)

```text
TÂCHE B1: Route /menu dans LocalCMS consumer
  ENDPOINT: GET /menu → lit opt_trading_menu.json
  RETOURNE: structure JSON complète

TÂCHE B2: Route /menu/state dans LocalCMS consumer
  ENDPOINT: GET /menu/state → lit state_cache.json
  RETOURNE: états actuels modules opérationnels

TÂCHE B3: Page navigation /menu
  HTML: sidebar avec 14 domaines
  CHAQUE DOMAINE: liste sous-menus + modules
  CHAQUE MODULE: badge état (●OUI ○IMPL ◌SPEC ✕CLOSED ⊕PROD)
  CLICK: → vue détail module
```

### PHASE C — Vue détail module

```text
TÂCHE C1: Page /menu/module/{id}
  AFFICHAGE:
    → nom, domaine, famille de consolidation
    → état (operational/impl/spec/closed/to_build)
    → machine hôte
    → structure (app/, cmd.sh, scripts/, docs/)
    → sanity status si disponible
    → GO associé si worker à produire
    → liens vers docs/ si présents
  SOURCE:
    → opt_trading_menu.json (structure)
    → state_cache.json (état live)
    → lecture README.md (statique, 1 fois)
```

### PHASE D — Vue pipeline (enrichissement dynamique)

```text
TÂCHE D1: Page /menu/pipeline
  AFFICHAGE:
    → flux signal → proposition → validation → trade → résultat → learning
    → état de chaque étape (worker existant ou PROD)
    → flèches connexion entre étapes
    → indicateur bloquant si étape manquante
  SOURCE:
    → état workers stricts (state_cache.json)
    → opt_trading_menu.json section workers

TÂCHE D2: Page /menu/desk-pipeline
  AFFICHAGE:
    → pipeline Desk Pro : Step 0 → A → B → D → E
    → état de chaque step (depuis state_cache)
    → dernier fichier produit (latest.json timestamp)
```

---

## GO REQUIS

```text
GO_OPENCLAW_OPT_TRADING_LOCALCMS_MENU_STATIC_01
  SCOPE: phases A + B — menu JSON + LocalCMS routes /menu + /menu/state
  PRÉREQ: aucun (indépendant de tous les workers)
  LIVRABLE: menu navigable dans LocalCMS avec états modules
  MACHINE: db-layer
  PARALLÈLE: peut ouvrir en même temps que GO_OPERATOR_BRIDGE

GO_OPENCLAW_OPT_TRADING_LOCALCMS_MENU_DETAIL_01
  SCOPE: phase C — vue détail module
  PRÉREQ: GO_LOCALCMS_MENU_STATIC_01
  LIVRABLE: page détail par module avec état live

GO_OPENCLAW_OPT_TRADING_LOCALCMS_PIPELINE_VIEW_01
  SCOPE: phase D — vue pipeline trading + desk pipeline
  PRÉREQ: GO_LOCALCMS_MENU_DETAIL_01 + au moins signal_router
  LIVRABLE: vue pipeline dynamique avec états workers
```

---

## INDICATEURS D'ÉTAT — CONVENTION

```text
● OUI       → opérationnel prouvé (cmd.sh + PASS documenté)
○ IMPL      → implémenté, runtime non prouvé
◌ SPEC      → spécifié seulement (doc sans impl)
⊕ PROD      → à produire (absent)
✕ CLOSED    → fermé définitif
↓ DEPRECATED → en cours de dépréciation
```

---

## REFRESH STRATEGY

```text
MENU STRUCTURE (opt_trading_menu.json):
  → statique, reload à chaque déploiement GO
  → pas de polling dynamique

ÉTATS MODULES (state_cache.json):
  → refresh 30s pour modules opérationnels (gateway, desk_pro, etc.)
  → refresh 5min pour modules non-critiques
  → côté serveur (cron ou tmux boucle) → LocalCMS lit le cache

VUE CLIENT:
  → auto-refresh 30s (JS polling GET /menu/state)
  → ou WebSocket si LocalCMS supporte (optionnel)
```

---

## RÉSUMÉ ARCHITECTURE COMPLÈTE

```text
DONNÉES:
  opt_trading_menu.json    ← structure menu 14 domaines
  state_schema.json        ← modules à surveiller + endpoints
  state_cache.json         ← états live (refresh 30s)
  ui_registry_msi/config/  ← enrichissement automatique surfaces UI

SCRIPTS:
  menu_state_aggregator.sh ← interroge health endpoints → state_cache.json

LOCALCMS ROUTES:
  GET /menu              → navigation 14 domaines
  GET /menu/state        → états live
  GET /menu/module/{id}  → détail module
  GET /menu/pipeline     → vue pipeline trading
  GET /menu/desk         → vue pipeline Desk Pro

TMUX:
  localcms-ui session    → LocalCMS consumer (pane lcms:consumer)
  openclaw-core session  → menu_state_aggregator boucle (pane core:health)
```
