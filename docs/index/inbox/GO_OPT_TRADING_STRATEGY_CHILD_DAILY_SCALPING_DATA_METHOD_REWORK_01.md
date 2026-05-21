---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-20
topic_keys:
  - daily_scalping
  - data_method
  - canonical_ohlcv
  - derivatives_collector
  - bot_vision
  - visual_context
  - choch_rework
  - backtest_protocol
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/10_PR658_METHOD_AUDIT.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/20_DATA_SOURCE_HIERARCHY.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/30_CANONICAL_OHLCV_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/40_COLLECTOR_INTEGRATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/50_BOT_VISION_VALIDATION_LAYER.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/60_REVISED_BACKTEST_PROTOCOL.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01

**État:** Open
**Branche:** `go/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01`
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`

Rework méthode backtest daily scalping : remplacer Yahoo Finance / GC=F (smoke)
par source canonique broker/prod collector avec bid/ask/spread, intégrer
derivatives_collector comme couche contextuelle, documenter bot vision comme
couche validation structurelle, réviser CHOCH proxy (multi-bar) et min_score
par variant.

PR #658 reclassée : `TECHNICAL_SMOKE_PASS` — pas un verdict stratégique.

## Docs chantier

- `00_INITIAL_PROJECT_DOC.md` — Cadrage + contexte PR #658
- `10_PR658_METHOD_AUDIT.md` — Audit des 5 défauts de méthode
- `20_DATA_SOURCE_HIERARCHY.md` — Hiérarchie source primaire → fallback → interdit
- `30_CANONICAL_OHLCV_CONTRACT.md` — Schéma CSV avec bid/ask/spread + validation
- `40_COLLECTOR_INTEGRATION_PLAN.md` — Branchement derivatives_collector
- `50_BOT_VISION_VALIDATION_LAYER.md` — Protocole visual_context comme evidence
- `60_REVISED_BACKTEST_PROTOCOL.md` — Pipeline complet post-rework + reworks code

## Reworks code requis

| Module | Rework |
|---|---|
| `detectors.py` | CHOCH fenêtre configurable (3-10 bars, pas same-bar) |
| `scorer.py` / `config.yaml` | `min_score_by_variant` par variant |
| `load_data.py` | validation source level — bloque smoke_yfinance pour verdict |
| `simulator.py` | spread depuis feed broker, pas config hardcodé |
| `report.py` | metadata source_level + regime_coverage dans verdict |

## Prérequis avant implémentation code

1. Obtenir source OHLCV canonique (MT5 export ou Dukascopy) minimum 6 mois
2. Confirmer granularité exports derivatives_collector (timestamp UTC, M5-compatible)
3. Calibrer `choch_confirm_window` sur données réelles
