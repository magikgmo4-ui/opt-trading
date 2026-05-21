---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-21
topic_keys:
  - daily_scalping
  - pullback_entry
  - limit_order
  - choch_level
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01/20_ACCEPTANCE_REPORT.md
  - tools/strategy/daily_scalping/detectors.py
  - tools/strategy/daily_scalping/simulator.py
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01

**État:** Open
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`

Entry sur pullback au CHOCH level (swing_h) plutôt qu'au close CHOCH bar.
Risk = structure range (swing_h - swing_l) au lieu de CHOCH_close - swing_l.
Cible : exp > 0R sur sessions actives.
