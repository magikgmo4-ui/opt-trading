---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01_CHAIN_CANONICAL_MAP
doc_type: chain_map
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/10_CHAIN_SURFACE_PROOF_MAP.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TELEGRAM_EVENT_ROUTING_MAP_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01/00_INITIAL_PROJECT_DOC.md
---

# 01_CHAIN_CANONICAL_MAP

## MASTER_TARGET

Produit final total voulu : une chaine totale composee de plusieurs chaines independantes mais liees, avec Desk Pro comme hub consumer et avec separation stricte entre Telegram inbound screener et Telegram outbound notification.

## Chaines confirmees / partiellement confirmees

### 1. Runtime operateur distant

| Surface | Preuve locale | Etat |
| --- | --- | --- |
| operator phone / SSH | `30_EXECUTION_PROTOCOL.md` decrit `ssh admin-trading` | PARTIAL_DOC_PROOF |
| tmux IDE | `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_OPERATOR_WORKFLOW_MINIMAL_01/30_EXECUTION_PROTOCOL.md` | PRESENT_DOC |
| OpenCode / OpenClaw runtime | references documentaires multiples ; `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` non localise sous ce nom | PARTIAL_DOC_PROOF |

### 2. TradingView Alert Chain

| Segment | Preuve locale | Etat |
| --- | --- | --- |
| TradingView -> webhook | `webhook_server.py`, `modules/webhook/`, `docs/product/guides/TRADINGVIEW_TELEGRAM_PIPELINE.md` | PRESENT |
| webhook -> signal_event | `state/events.jsonl`, `signal_event` dans `20_INPUT_CONSUMER_MAP.md` | PRESENT |
| signal_event -> workers | `modules/signal_router/`, `proposition_engine`, `validation_gate`, `trade_executor`, `result_tracker`, `datasheet_writer`, `learning_feeder` | PRESENT |
| workers -> Desk Pro | `docs/chantiers/GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01/10_CHAIN_SURFACE_PROOF_MAP.md` | PRESENT |
| Desk Pro -> Telegram/Sheets/Perf | outbound/consumer surfaces presentes mais chainage total encore incomplet | PARTIAL |

### 3. Bot Vision / Headless Screener Chain

| Segment | Preuve locale | Etat |
| --- | --- | --- |
| headless capture | `modules/bot_vision/headless_capture/`, `capture_headless.js` | PRESENT |
| vision consumer | `modules/vision_bot/`, `modules/bot_vision_step2/`, `docs/product/guides/BOT_VISION.md` | PRESENT |
| artefacts Desk Pro / Telegram | guide Bot Vision + references Desk Pro / Telegram | PARTIAL |

### 4. Telegram Screener Inbound Chain

| Segment | Preuve locale | Etat |
| --- | --- | --- |
| registry channels inbound | `docs/chantiers/GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01/10_CURRENT_INBOUND_SURFACES.md` | DOC_PRESENT |
| ingest/parsers screener trades-setups | pas de parser inbound prouve | GAP |
| replay/backtest scoring | `scripts/telegram/latency_backtest.py` et docs latency presentes ; inbound screener non chaine completement | PARTIAL |

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

`GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01`

## Gaps encore ouverts

- separation inbound/outbound Telegram a conserver dans tous les enfants
- desk pro hub scoring total encore a contractualiser chaine par chaine
- collectors Coinglass / exchange APIs a recroiser plus finement dans l'inventaire parent
- E2E dry-run total umbrella non qualifie dans ce parent
- closeout final umbrella impossible a ce stade
