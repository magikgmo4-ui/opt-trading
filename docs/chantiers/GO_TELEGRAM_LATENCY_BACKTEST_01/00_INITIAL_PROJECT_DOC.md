---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: active
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/10_CURRENT_SURFACES_AND_TELEMETRY.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/20_METHODOLOGY_AND_METRICS.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/30_BACKTEST_OUTPUT_SCHEMA.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/40_GAPS_AND_NEXT_GO.md
  - docs/chantiers/GO_TELEGRAM_LATENCY_BACKTEST_01/90_REPRISE_POINT.md
---

# 00_INITIAL_PROJECT_DOC - Telegram latency backtest

## MASTER_TARGET

Ce child contribue au produit final total voulu par le parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01`, avec
separation stricte entre :

- Telegram notification outbound multi-destinations
- Telegram screener inbound
- TradingView/webhook -> signal_event -> Desk Pro -> Telegram/Sheets/Perf
- Bot Vision / headless screener
- Google Sheets global
- Strategy Registry / Perf Engine / replay / paper

## But

Quantifier la latence Telegram du produit (sendMessage) en conditions contrôlées:

- stats par surface (notification_dispatcher / webhook / desk alerts)
- stats globales (p50/p90/p95/p99)
- base pour “reaction strategy” (latency gating) sans MEV/mempool

## Contraintes

- aucune dépendance à un listener inbound Telegram (pas de getUpdates)
- pas de secrets dans le repo
- doc + instrumentation minimale + script d’analyse offline

## Livrables

- inventaire surfaces + telemetry
- méthodologie et métriques
- backtest script (JSONL → summary)

## Regle Kanban / continuite

Le tableau Kanban du bundle reste la carte de navigation principale. Ce child
documente la latence Telegram outbound du produit final total et ne remplace
pas le Kanban bundle par une roadmap concurrente.

## Prochain item Kanban a faire

`GO_PERF_ENGINE_STRATEGY_SCORE_01`

## Gaps encore ouverts

- pas de mesure de reception client Telegram end-to-end
- pas de retry policy standard par tier
- pas de branchement latency -> Perf Engine / Strategy Registry
