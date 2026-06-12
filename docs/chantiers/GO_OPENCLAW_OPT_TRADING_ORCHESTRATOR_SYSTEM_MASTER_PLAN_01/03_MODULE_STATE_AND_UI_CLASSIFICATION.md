---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_MODULE_CLASSIFICATION
doc_type: classification
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-14
---

# 03_MODULE_STATE_AND_UI_CLASSIFICATION

## Axes de classification

```
A — DOCUMENTÉ      : doc/chantier présent sur sot/mainline
B — IMPLÉMENTÉ     : code existant (app/, cmd.sh, sanity.sh prouvés)
C — OPÉRATIONNEL   : runtime prouvé (PASS documenté ou cmd.sh validé)
D — À PRODUIRE     : absent ou spécifié seulement
E — À CONSOLIDER   : famille fragmentée constituant un seul produit
F — UI/APP VISUEL  : branché à une interface visuelle ou web
G — NON UI         : data/compute/infra sans surface visuelle directe
```

---

## FAMILLES FRAGMENTÉES — À CONSOLIDER (axe E)

Ces modules constituent un seul produit mais sont répartis en plusieurs versions ou sous-modules.
Un GO de consolidation est requis avant ou en parallèle des travaux d'orchestration.

### E1 — Famille Desk Pro (1 produit, ~10 modules)

```
PRODUIT: Desk Pro — système de trading observation et décision
MODULES:
  desk_pro              → cœur API/UI (FastAPI routes + page.py + mount.py) — CENTRE DE GRAVITÉ
  desk_pro_runner       → façade opératoire (cmd.sh, menu.sh, sanity_check.sh, run/run-and-show)
  desk_pro_orchestrator → conductor pipeline (cmd.sh, séquence déterministe)
  desk_pro_dashboard    → dashboard visualisation
  desk_analyze          → analyse
  desk_capture_inputs   → capture inputs
  desk_common           → shared
  desk_retention        → rétention données
  desk_snapshot_ingest  → ingestion snapshots
  desk_state            → state management

CONSOLIDATION REQUISE: oui
POINT D'ENTRÉE CANONIQUE: desk_pro_runner (cmd.sh run / run-and-show)
UI: OUI — desk_pro expose FastAPI + HTML dashboard
ÉTAT: IMPLÉMENTÉ, partiellement opérationnel (smoke PASS admin-trading)
```

### E2 — Famille Perf (1 produit, 2 modules + shim)

```
PRODUIT: Perf — tracking performance simulation (paper)
MODULES:
  perf        → shim compat-first (app.py → perf/perf_app.py, webhook.py → adapter, engine/ → perf_engine)
  perf_engine → moteur réel (tracking ideas paper, scripts/cmd.sh)

CONSOLIDATION REQUISE: oui (perf est un wrapper de migration vers perf_engine)
POINT D'ENTRÉE CANONIQUE: perf/scripts/cmd.sh (jusqu'à migration complète)
UI: OUI — perf_app.py est une app web, intégré dans desk_pro via mount
ÉTAT: IMPLÉMENTÉ, shim en cours de migration
```

### E3 — Famille Vision/Bot (1 produit, 3 modules)

```
PRODUIT: Bot Vision — capture et analyse visuelle screenshot trading
MODULES:
  bot_vision       → impl principale (smoke PASS admin-trading)
  bot_vision_step2 → step2 (app/, FastAPI)
  vision_bot       → variante alternative (app/)

CONSOLIDATION REQUISE: oui
POINT D'ENTRÉE CANONIQUE: bot_vision (principal)
UI: OUI — analyse visuelle screenshots, connecté desk_pro
ÉTAT: bot_vision OPÉRATIONNEL (admin-trading), step2/vision_bot statut inconnu
```

### E4 — Famille OpenClaw (1 runtime, 8 modules)

```
PRODUIT: OpenClaw runtime — gateway + agent + config + menus
MODULES:
  gateway_openclaw       → scripts cmd.sh/start/stop/health — OPÉRATIONNEL
  menu_openclaw          → menus CLI (app/, docs/, scripts/)
  model_provider_openclaw → provider routing modèle
  configure_openclaw     → configuration runtime
  doctor_openclaw        → diagnostic
  evidence_openclaw      → collecte preuves runtime
  install_module_openclaw → installation
  openclaw_config_modulaire → config modulaire (app/, docs/, scripts/)

CONSOLIDATION REQUISE: oui — 8 modules pour 1 runtime
POINT D'ENTRÉE CANONIQUE: gateway_openclaw (cmd.sh) + menu_openclaw (menus)
UI: NON (CLI uniquement, loopback ws://127.0.0.1:18789)
ÉTAT: gateway OPÉRATIONNEL — autres modules impl partielle
```

### E5 — Famille Market Data (1 pipeline, 7 modules)

```
PRODUIT: Market data pipeline — collecte et analyse marché
MODULES:
  marketdata           → hub données (app/)
  market_scanner       → scan opportunités → feed probability_engine
  collector_binance_spot → collecte Binance (impl V1 minimal)
  collector_coingecko  → collecte CoinGecko
  derivatives_collector → collecte dérivés
  derivatives_analyzer → analyse dérivés (app/)
  liquidation_analyzer → analyse liquidations (app/)

CONSOLIDATION REQUISE: oui — pipeline unifié requis
POINT D'ENTRÉE CANONIQUE: market_scanner (orchestre les collectors)
UI: NON (data pipeline)
ÉTAT: collector_binance_spot impl V1 ; autres statut inconnu
```

### E6 — Famille SSH/Réseau (1 surface, 3 couches)

```
PRODUIT: reseau_ssh — connectivité SSH multi-machine
MODULES:
  reseau_ssh       → CANONIQUE (modules/reseau_ssh/scripts/) — OPÉRATIONNEL
  reseau_ssh_step1b → compat (à réduire)
  scripts/reseau_ssh → héritage (à réduire)

CONSOLIDATION REQUISE: oui (GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 ouvert)
POINT D'ENTRÉE CANONIQUE: modules/reseau_ssh/
UI: NON (infra)
ÉTAT: reseau_ssh OPÉRATIONNEL, step1b/scripts en dépréciation progressive
```

### E7 — Famille Registres/Readers (1 surface, 5 modules)

```
PRODUIT: registry system — lecture registres modules/machines/wrappers
MODULES:
  registry_router
  registry_meta_reader
  modules_registry_reader
  machines_registry_reader
  wrappers_registry_reader

CONSOLIDATION REQUISE: oui — 5 readers pour 1 surface registre
UI: NON (infra interne)
ÉTAT: impl (app/ présent), statut opérationnel inconnu
```

### E8 — Famille DeepSeek (1 provider, 4 modules)

```
PRODUIT: DeepSeek — provider IA alternatif à OpenClaw
MODULES:
  deepseek_hub      → hub (app/)
  deepseek_response → handling réponses
  deepseek_student  → CLOSED (surface student fermée)
  deepseek_thinking → mode thinking

CONSOLIDATION REQUISE: oui (deepseek_student à archiver)
UI: NON (provider IA)
ÉTAT: deepseek_student CLOSED ; hub/response/thinking statut inconnu
```

### E9 — Famille Ops Menus (1 surface, 3 modules)

```
PRODUIT: ops menus — menus opérateur CLI
MODULES:
  ops_menu_hub
  ops_super_menu
  ops_wrappers / ops_wrappers.bak

CONSOLIDATION REQUISE: oui (ops_wrappers.bak = dette)
UI: CLI uniquement
ÉTAT: impl, opérationnel probable
```

### E10 — Famille Shared/Transfer (1 surface, 3 modules)

```
PRODUIT: transfert fichiers inter-machines
MODULES:
  shared             → fichiers partagés
  shared_files_sftp  → SFTP
  shared_sshfs_permanent → SSHFS permanent

CONSOLIDATION REQUISE: à vérifier
UI: NON (infra)
ÉTAT: impl, opérationnel probable (dépend de reseau_ssh)
```

---

## TABLEAU COMPLET — ÉTAT PAR MODULE

### TRADING / EXECUTION

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `execution_engine` | non | ✓ app/ | non prouvé | worker trade_executor | E1 → desk_pro | NON |
| `decision_engine` | non | ✓ app/ | non prouvé | wrapper proposition | E1 → desk_pro | NON |
| `risk_engine` | non | ✓ app/ | non prouvé | wrapper validation_gate | E1 → desk_pro | NON |
| `position_engine` | non | ✓ app/ | non prouvé | worker result_tracker | E1 → desk_pro | NON |
| `portfolio_engine` | non | ✓ app/ | non prouvé | worker result_tracker | E1 → desk_pro | NON |
| `opportunity_ranker` | non | ✓ app/ | non prouvé | wrapper proposition | E1 → desk_pro | NON |
| `probability_engine` | non | ✓ app/ | non prouvé | wrapper proposition | E1 → desk_pro | NON |
| `kil_v1` | partiel | ✓ cmd.sh | **OUI** (cmd.sh) | brancher validation_gate | seul | NON |
| `trading_realtime_v1` | non | ✓ app/ | non prouvé | observation seule | seul | NON |
| `trading_lab_v1` | non | ✓ app/ | non prouvé | smoke/test | seul | NON |
| `simex_bitget_bridge` | ✓ | ✓ cmd.sh sanity | **OUI** (contrat SIMEX_UNITS_V1) | brancher trade_executor | seul | NON |
| `webhook` | partiel | ✓ handlers.py | non prouvé | brancher signal_router | seul | NON |

### MARKET DATA

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `marketdata` | non | ✓ app/ | non prouvé | brancher signal_router | E5 | NON |
| `market_scanner` | non | ✓ app/ | non prouvé | brancher signal_router | E5 | NON |
| `collector_binance_spot` | non | ✓ V1 minimal | **PARTIEL** | brancher marketdata | E5 | NON |
| `collector_coingecko` | non | ✓ app/ | non prouvé | brancher marketdata | E5 | NON |
| `derivatives_collector` | non | ✓ app/ | non prouvé | brancher marketdata | E5 | NON |
| `derivatives_analyzer` | non | ✓ app/ | non prouvé | brancher enrichissement | E5 | NON |
| `liquidation_analyzer` | non | ✓ app/ | non prouvé | brancher enrichissement | E5 | NON |

### DESK PRO / UI

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `desk_pro` | ✓ | ✓ API+page.py | **OUI** (actif) | point d'entrée UI prod | E1 | **OUI** — FastAPI + HTML |
| `desk_pro_runner` | ✓ | ✓ cmd.sh run | **OUI** (cmd.sh) | façade opératoire | E1 | **OUI** (via desk_pro) |
| `desk_pro_orchestrator` | ✓ | ✓ cmd.sh | **OUI** (cmd.sh) | pipeline conductor | E1 | **OUI** (via desk_pro) |
| `desk_pro_dashboard` | ✓ | ✓ app/ | non prouvé | dashboard | E1 | **OUI** |
| `desk_analyze` | non | partiel | non prouvé | analyse | E1 | **OUI** (via desk_pro) |
| `desk_capture_inputs` | non | partiel | non prouvé | capture | E1 | **OUI** (via desk_pro) |
| `desk_common` | non | partiel | non prouvé | shared | E1 | **OUI** (via desk_pro) |
| `desk_retention` | non | partiel | non prouvé | rétention | E1 | **OUI** (via desk_pro) |
| `desk_snapshot_ingest` | non | partiel | non prouvé | ingestion | E1 | **OUI** (via desk_pro) |
| `desk_state` | non | partiel | non prouvé | state | E1 | **OUI** (via desk_pro) |
| `perf` | ✓ | ✓ shim cmd.sh | **OUI** (shim) | migration → perf_engine | E2 | **OUI** — perf_app.py |
| `perf_engine` | non | ✓ app/ | non prouvé | tracking paper | E2 | **OUI** (via perf) |
| `journal_engine` | non | ✓ app/ | non prouvé | datasheet_writer | seul | **OUI** (via desk_pro) |
| `bot_vision` | ✓ | ✓ app/ | **OUI** (admin-trading) | vision prod | E3 | **OUI** — screenshots |
| `bot_vision_step2` | non | ✓ app/ FastAPI | non prouvé | vision avancée | E3 | **OUI** |
| `vision_bot` | non | ✓ app/ | non prouvé | alternative | E3 | **OUI** |

### AI / MODÈLES

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `validated_prompt_factory` | ✓ | ✓ cmd.sh sanity | **OUI** | prompt_generator | seul | NON (CLI) |
| `memory_bricks` | ✓ | ✓ cmd.sh sanity | **OUI** (cmd.sh) | learning store | seul | NON |
| `workflow_post_change_v2` | non | ✓ scripts/ | non prouvé | post-change hook | seul | NON |
| `deepseek_hub` | non | ✓ app/ | non prouvé | provider alt | E8 | NON |
| `deepseek_response` | non | ✓ app/ | non prouvé | provider alt | E8 | NON |
| `deepseek_thinking` | non | ✓ app/ | non prouvé | provider alt | E8 | NON |
| `deepseek_student` | non | ✓ | CLOSED | archiver | E8 | NON |
| `hf_free_platform` | non | ✓ app/ | non prouvé | provider HF | seul | NON |
| `mimo_open_observer` | non | ✓ cmd.sh | CLOSED (student) | archiver | seul | NON |

### OPENCLAW

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `gateway_openclaw` | ✓ | ✓ cmd.sh complet | **OUI** | backbone | E4 | NON (ws loopback) |
| `menu_openclaw` | partiel | ✓ scripts/ | partiel | menus | E4 | NON (CLI) |
| `model_provider_openclaw` | partiel | ✓ app/ | non prouvé | routing modèle | E4 | NON |
| `configure_openclaw` | non | ✓ scripts/ | non prouvé | config | E4 | NON |
| `doctor_openclaw` | non | ✓ scripts/ | non prouvé | diagnostic | E4 | NON |
| `evidence_openclaw` | non | ✓ scripts/ | non prouvé | preuves | E4 | NON |
| `install_module_openclaw` | non | ✓ app/ | non prouvé | install | E4 | NON |
| `openclaw_config_modulaire` | non | ✓ app/ scripts/ | non prouvé | config modulaire | E4 | NON |
| `tradingview_observer_openclaw` | non | ✓ run.ps1 | non prouvé | TV + OpenClaw bridge | E4 | Partiel (Windows) |
| `openclaw_operator_bridge` | ✓ SPEC | ✗ | **NON** | **PRIORITÉ 1** | nouveau | NON |

### TRADINGVIEW / WEBHOOK

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `tradingview_observer` | ✓ | ✓ app/ + export | **OUI** (admin-trading, Windows) | signal_router amont | seul | **OUI** (Windows, PS1) |
| `webhook` | ✓ | ✓ handlers.py | non prouvé | signal_router amont | seul | NON (interne) |

### INFRA / CONNECTIVITY

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `reseau_ssh` | ✓ | ✓ scripts/ | **OUI** | backbone multi-machine | E6 | NON |
| `reseau_ssh_step1b` | non | ✓ | compat | archiver | E6 | NON |
| `shared_files_sftp` | non | ✓ | non prouvé | transfert | E10 | NON |
| `shared_sshfs_permanent` | non | ✓ | non prouvé | transfert | E10 | NON |
| `winscp_transfer` | non | ✓ | non prouvé | transfert Windows | seul | NON |
| `auth` | non | ✓ | non prouvé | sécurité | seul | NON |
| `health` | non | ✓ | non prouvé | monitoring | seul | NON |
| `git_fleet_guard` | non | ✓ app/ | non prouvé | guard | seul | NON |
| `repo_hygiene` | non | ✓ | non prouvé | maintenance | seul | NON |

### OPS MENUS

| Module | Doc | Impl | Opérationnel | À produire | À consolider | UI |
| --- | --- | --- | --- | --- | --- | --- |
| `ops_menu_hub` | non | ✓ | non prouvé | menu central | E9 | NON (CLI) |
| `ops_super_menu` | non | ✓ | non prouvé | super menu | E9 | NON (CLI) |
| `ops_wrappers` | non | ✓ | non prouvé | wrappers ops | E9 | NON (CLI) |
| `module_contextuals_shell` | non | ✓ cmd.sh | non prouvé | contextuals | seul | NON |
| `naming_normalizer` | non | ✓ cmd.sh sanity | non prouvé | naming | seul | NON |

---

## VUE SYNTHÉTIQUE — BRANCHÉ UI vs NON UI

### Branché UI / App visuelle

```text
SURFACE WEB / FASTAPI:
  desk_pro          → FastAPI + HTML (centre de gravité Desk Pro)
  desk_pro_dashboard → dashboard web
  perf / perf_engine → app web (perf_app.py)
  bot_vision_step2  → FastAPI

SURFACE VISUELLE / SCREENSHOT:
  bot_vision        → capture + analyse screenshots trading
  tradingview_observer → TradingView interface (Windows/PS1)

APPS EXTERNES:
  TradingView       → webhooks + alertes visuelles
  Telegram          → notifications + commandes opérateur
  Botpress          → bot conversationnel
  ClickUp           → UI task management
  Airtable          → UI data tables
  Figma             → UI design (différé)
  LocalCMS          → UI lecture web (db-layer consumer)
```

### Non branché UI — Data / Compute / Infra / CLI

```text
PIPELINE TRADING (compute):
  execution_engine, decision_engine, risk_engine
  position_engine, portfolio_engine
  opportunity_ranker, probability_engine, kil_v1
  simex_bitget_bridge, trading_realtime_v1, trading_lab_v1
  webhook

MARKET DATA (data):
  marketdata, market_scanner, collector_binance_spot
  collector_coingecko, derivatives_collector
  derivatives_analyzer, liquidation_analyzer

OPENCLAW (runtime CLI/ws):
  gateway_openclaw, menu_openclaw, model_provider_openclaw
  configure_openclaw, doctor_openclaw, evidence_openclaw
  install_module_openclaw, openclaw_config_modulaire

AI / MODELS (providers CLI):
  validated_prompt_factory, memory_bricks
  deepseek_hub, deepseek_response, deepseek_thinking
  hf_free_platform, workflow_post_change_v2

INFRA (infrastructure):
  reseau_ssh, shared_*, winscp_transfer
  auth, health, git_fleet_guard
  registry_router, registry_meta_reader
  modules_registry_reader, machines_registry_reader
  wrappers_registry_reader, naming_normalizer
  module_contextuals_shell, trae_module_validator

OPS MENUS (CLI):
  ops_menu_hub, ops_super_menu, ops_wrappers
```

---

## CE QUI EST À PRODUIRE (manquant ou non démarré)

### Workers pipeline orchestration

```text
signal_router              → normalise webhook TradingView → JSON
proposition_engine         → wraps decision_engine + OpenClaw builder
validation_gate            → wraps risk_engine + kil_v1 + Telegram
trade_executor             → wraps execution_engine + simex_bitget_bridge
result_tracker             → wraps position_engine + portfolio_engine
datasheet_writer           → wraps journal_engine → Sheets + Airtable
learning_feeder            → wraps memory_bricks + OpenClaw builder
notification_dispatcher    → Telegram structuré par étape pipeline
task_tracker               → ClickUp sync
```

### Modules manquants

```text
openclaw_operator_bridge   → SPEC COMPLÈTE — IMPL MANQUANTE (PRIORITÉ 1)
sheets_writer              → NON INITIÉ
db_ingestion_pipeline      → governance docs existants — impl manquante
```

### Docs manquantes (modules sans doc)

```text
~40 modules sans chantier documentaire :
  execution_engine, decision_engine, risk_engine, position_engine,
  portfolio_engine, opportunity_ranker, probability_engine,
  marketdata, market_scanner, collectors, liquidation_analyzer,
  desk_state, desk_analyze, desk_capture_inputs, desk_common,
  desk_retention, desk_snapshot_ingest, perf_engine, journal_engine,
  deepseek_*, hf_free_platform, configure_openclaw, doctor_openclaw,
  evidence_openclaw, auth, health, registry_*, shared_*, …
```

---

## CE QUI EST À CONSOLIDER (priorité par impact)

| Famille | Priorité | Action |
| --- | --- | --- |
| E1 — Desk Pro | HAUTE | Valider état opérationnel complet ; point d'entrée = desk_pro_runner |
| E4 — OpenClaw | HAUTE | Implémenter openclaw_operator_bridge ; consolider 8 modules → 1 runtime |
| E5 — Market Data | HAUTE | Valider pipeline collector → market_scanner → signal_router |
| E6 — reseau_ssh | EN COURS | GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03 ouvert |
| E2 — Perf | MOYENNE | Compléter migration perf shim → perf_engine |
| E3 — Vision/Bot | MOYENNE | Clarifier survie bot_vision vs vision_bot vs step2 |
| E7 — Registres | BASSE | Regrouper sous 1 surface registry |
| E8 — DeepSeek | BASSE | Archiver deepseek_student ; clarifier hub/response/thinking |
| E9 — Ops menus | BASSE | Regrouper ops_menu_hub + super_menu |
| E10 — Shared | BASSE | Valider SFTP/SSHFS opérationnel |

## RISKS

- À qualifier.
