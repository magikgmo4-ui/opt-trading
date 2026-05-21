---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-21
topic_keys:
  - daily_scalping
  - entry_quality
  - sl_placement
  - session_filter
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01/20_ACCEPTANCE_REPORT.md
  - tools/strategy/daily_scalping/detectors.py
  - tools/strategy/daily_scalping/simulator.py
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01

**État:** Open
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`

Fix SL placement (sous le swept level) + filtre sessions asia/off.
Baseline : SMC_SWEEP exp=-0.19R. Cible : exp > 0R.
