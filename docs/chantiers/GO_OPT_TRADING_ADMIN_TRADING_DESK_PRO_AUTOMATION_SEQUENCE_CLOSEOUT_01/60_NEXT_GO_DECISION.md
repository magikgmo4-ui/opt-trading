---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01_NEXT_GO
doc_type: next_go_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_SEQUENCE_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-11
---

# 60_NEXT_GO_DECISION - Next GO Decision

## Recommended next GO

1. `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_PR_MERGE_01`

Reason:
Canoniser toute la sequence automation vers `sot/mainline` avant toute extension plus risquee.

## Only after merge

1. `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01`
2. `GO_OPT_TRADING_ADMIN_TRADING_LIVE_RUNTIME_SMOKE_GATED_01`
3. `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PLAYWRIGHT_SETUP_01`

## Guardrail

Ne pas recommander de live smoke avant merge de la sequence automation.

## RISKS

- À qualifier.
