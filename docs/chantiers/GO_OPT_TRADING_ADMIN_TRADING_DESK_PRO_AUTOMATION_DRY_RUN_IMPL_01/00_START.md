---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01_START
doc_type: start
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 00_START - Desk Pro Automation Dry Run Impl

## GO ID

`GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_DRY_RUN_IMPL_01`

## Base branch

`origin/go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PLAN_01 @ da2360e`

## Objectif

Implementer un point d'execution Desk Pro dry-run, local et sans side effects runtime, capable de consommer `signal_event`, `visual_context` et `desk_snapshot` pour produire une synthese testable.

## Invariants

- patch minimal
- dry-run uniquement
- aucun trade
- aucun Telegram
- aucun webhook reel
- aucun systemd
- aucun timer
- aucun `.env` lu ou affiche

## Side effects attendus

`NONE`

## RISKS

- À qualifier.
