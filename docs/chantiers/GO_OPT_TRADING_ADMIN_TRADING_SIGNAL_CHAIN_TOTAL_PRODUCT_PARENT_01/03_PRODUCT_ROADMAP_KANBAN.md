---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01_PRODUCT_ROADMAP_KANBAN
doc_type: kanban_mirror
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-20
---

# 03_PRODUCT_ROADMAP_KANBAN

## Regle

Le tableau Kanban du bundle reste la carte de navigation principale.

Ce fichier est un miroir de continuite local, construit uniquement a partir :

- des items demands par le prompt initial
- des GOs locaux effectivement trouves
- des gaps prouves dans le repo

Il ne remplace pas `08_KANBAN_ROADMAP_PRODUIT_FINAL.md`.

## MASTER_TARGET / produit final total

Livrer le produit final total de toute la chaine signal/screener/Telegram/Desk Pro/Perf/Sheets/runtime sans fermer le parent umbrella avant livraison complete ou blocage explicite des surfaces critiques.

## Kanban miroir

| Ordre | Item bundle / chantier cible | Etat local | Preuve locale / GO associe |
| --- | --- | --- | --- |
| 1 | Runtime operateur distant (mapping local du bundle runtime) | OPEN_LOCAL_EQUIVALENT | `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` (operationnel) + `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` (historique) |
| 2 | Repo inventory umbrella | DOC_ALIGNED | `GO_STRATEGY_SIGNAL_MONITORING_REPO_INVENTORY_01` |
| 3 | Event taxonomy transverse | DOC_ALIGNED | `GO_EVENT_TAXONOMY_01` |
| 4 | Telegram routing outbound multi-destinations | DOC_ALIGNED | `GO_TELEGRAM_EVENT_ROUTING_MAP_01` |
| 5 | Desk Pro hub input expansion | DOC_ALIGNED | `GO_DESKPRO_INPUT_EXPANSION_01` |
| 6 | Telegram screener inbound registry | DOC_ALIGNED | `GO_TELEGRAM_SCREENER_CHANNEL_REGISTRY_01` |
| 7 | Google Sheets global schema | DOC_ALIGNED | `GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01` |
| 8 | Telegram latency / public-call backtest | DOC_ALIGNED | `GO_TELEGRAM_LATENCY_BACKTEST_01` |
| 9 | Strategy registry latency integration | DOC_ALIGNED | `GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01` |
| 10 | Perf engine strategy score | DOC_ALIGNED | `GO_PERF_ENGINE_STRATEGY_SCORE_01` |
| 11 | Signal chain E2E dry-run | ACTIVE_FIXTURE_PASS | `GO_SIGNAL_CHAIN_E2E_DRY_RUN_01` |
| 12 | Final closeout umbrella | BLOCKED_BY_OPEN_SURFACES | parent current GO |

## Surfaces majeures a ne pas considerer comme fermees

- TradingView webhook -> Desk Pro
- Bot Vision headless screener
- Coinglass / API collectors
- Telegram Screener inbound
- Telegram Notification outbound multi-chats/bots
- Desk Pro hub scoring
- Google Sheets global schema / implementation
- Strategy Registry integration
- Perf Engine / replay / paper / backtest
- Telegram latency / public-call backtest strategy
- E2E dry-run
- final closeout

## Prochain item Kanban exact

`GO_SIGNAL_CHAIN_E2E_DRY_RUN_01`

## Prochain GO exact

`GO_SIGNAL_CHAIN_E2E_DRY_RUN_01`

## Gaps encore ouverts

- le bundle local n'expose pas l'artefact exact `08_KANBAN_ROADMAP_PRODUIT_FINAL.md`
- `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01` est retrouve localement, mais reste a recroiser proprement avec le mapping runtime du parent umbrella ; la validation runtime reelle SSH/tmux/mobile reste PENDING via `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`
- sous-lots runtime `GO_OPT_TRADING_OPENCLAW_TMUX_OPERATOR_IMPL_01` et `GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01` recales sur preuves locales Python, mais la validation distantes SSH + device mobile reel restent PENDING
- E2E fixture-only umbrella passe, mais closeout total reste interdit tant que les fixtures ne sont pas converties en preuves reelles ou blocages explicites
- plusieurs surfaces restent ouvertes reellement: runtime distant, Bot Vision/headless, collectors Coinglass/API, routing final multi-destinations, implementation Sheets globale, closeout umbrella
