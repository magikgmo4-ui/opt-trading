---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-21
topic_keys:
  - daily_scalping
  - smc_choch
  - detectors
  - multi_bar_confirmation
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01/10_DESIGN.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01/20_ACCEPTANCE_REPORT.md
  - tools/strategy/daily_scalping/detectors.py
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01

**État:** Open
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`

Rework CHOCH detection : fenêtre de confirmation 0-5 barres au lieu du même-bar.

## Problème

Backtest canonique Dukascopy 2 ans → seulement 25 trades SMC. Cause : CHOCH exigé dans la même barre M5 que la récupération du sweep (probabilité ~12/an).

## Livrable

`detectors.py` — `detect_smc_sweep_only()` et `detect_combined()` avec `confirm_window=5`.

## Verdict attendu

SMC_SWEEP ≥ 100 trades → verdict statistiquement valide.
