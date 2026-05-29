---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01_CHAIN_CANONICAL_MAP
doc_type: chain_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/10_CHAIN_SURFACE_PROOF_MAP.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01/00_PARENT_CADRAGE.md
---

# 01_CHAIN_CANONICAL_MAP

## MASTER_TARGET

Produit final total voulu : une chaine totale composee de plusieurs chaines independantes mais liees, avec Desk Pro comme hub consumer et avec separation stricte entre Telegram inbound screener et Telegram outbound notification.

## Chaines confirmees / partiellement confirmees

### 1. Runtime operateur distant

| Surface | Preuve locale | Etat |
| --- | --- | --- |
| registry channels inbound | `modules/telegram_screener/registry/` + `channels.yaml` | RUNTIME_PRESENT (22 tests) |
| ingest/parsers screener trades-setups | `modules/telegram_screener/parser/` (trade, news, alpha parsers) | RUNTIME_PRESENT (32 tests) |
| signal producer + Desk Pro adapter | `modules/telegram_screener/signal/` (telegram_claim.v1) | RUNTIME_PRESENT (18 tests) |
| filtrage/routage | `modules/telegram_screener/router/` (FilterRouter, 5 rules) | RUNTIME_PRESENT (23 tests) |
| pipeline wiring | `modules/telegram_screener/pipeline/` (ScreenerPipeline) | RUNTIME_PRESENT (21 tests) |
| Telegram ingestion | `modules/telegram_ingestion/` (InboundClient, normalizer, router, Telethon) | RUNTIME_PRESENT (62 tests) |
| replay/backtest scoring | `scripts/telegram/latency_backtest.py` et docs latency presentes | PARTIAL |

### 5. Telegram Notification Outbound Chain

| Segment | Preuve locale | Etat |
| --- | --- | --- |
| helper Telegram | `shared/telegram_notify.py` | PRESENT |
| dispatcher outbound | `modules/notification_dispatcher/app/dispatcher.py` | PRESENT |
| routing multi chats/bots/topics | chantier `GO_TELEGRAM_EVENT_ROUTING_MAP_01` | DOC_PRESENT_PARTIAL |

### 6. Google Sheets Global

| Segment | Preuve locale | Etat |
| --- | --- | --- |
| daily sync borne | `scripts/sheets/sync_daily_session.py` | PRESENT_BOUNDED |
| schema global transverse | `GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01` | DOC_PRESENT |
| implementation globale | non ouverte a cette passe | GAP |

### 7. Strategy Registry / Perf Engine

| Segment | Preuve locale | Etat |
| --- | --- | --- |
| strategy registry | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/95_STRATEGY_REGISTRY.md` | PRESENT_DOC |
| perf engine | `modules/perf_engine/app/perf_engine.py` + tests | PRESENT |
| replay / paper / backtest | `modules/trading_lab_v1/`, `scripts/telegram/latency_backtest.py`, docs paper/regression diverses | PRESENT_PARTIAL |

## Kanban bundle conserve

Le tableau Kanban du bundle reste la reference principale. Ce fichier ne remplace pas `08_KANBAN_ROADMAP_PRODUIT_FINAL.md`; il consolide seulement les preuves locales par chaine.

## Prochain item Kanban a faire

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` (runtime distant)
— Ou `PF_BOT_VISION_HEADLESS` (vision/headless closeout)

## Gaps encore ouverts (post-closeout)

- separation inbound/outbound Telegram a conserver dans tous les enfants
- desk pro hub scoring total encore a contractualiser chaine par chaine
- collectors Coinglass / exchange APIs a recroiser plus finement dans l'inventaire parent
- E2E dry-run umbrella qualifie en fixture-only, writers reeles restent absents
- Bot Vision / headless screener closeout pending
