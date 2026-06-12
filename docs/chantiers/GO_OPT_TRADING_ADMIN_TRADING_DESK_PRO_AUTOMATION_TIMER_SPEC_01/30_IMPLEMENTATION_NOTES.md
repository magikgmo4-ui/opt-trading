---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01_IMPL_NOTES
doc_type: implementation_notes
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 30_IMPLEMENTATION_NOTES - Implementation Notes

## GO.scope

TIMER_SPEC = **docs-only**. Pas d'implementation runtime.

## Ce qui reste a faire

1. Creer `modules/desk_pro/systemd/`
2. Creer `desk_pro_dry_run.timer`
3. Creer `desk_pro_dry_run.service`
4. Creer `desk_pro_dry_run.sh` wrapper
5. Activer timer (dans TIMER_IMPL GO)

## Decision

- Timer spec est documentee
- Implementation differee a TIMER_IMPL
- Cela permet review separate avant implementation

## RISKS

- À qualifier.
