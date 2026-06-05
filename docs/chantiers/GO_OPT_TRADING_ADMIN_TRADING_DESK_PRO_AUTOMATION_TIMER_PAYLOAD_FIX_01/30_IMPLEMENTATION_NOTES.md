---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01_IMPLEMENTATION
doc_type: implementation_notes
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_PAYLOAD_FIX_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 30_IMPLEMENTATION_NOTES - Implementation Notes

## Files patched

- `modules/desk_pro/desk_pro_dry_run.sh`
- `modules/desk_pro/dry_run.py`
- `tests/test_desk_pro_dry_run.py`

## Patch summary

- script switched from partial pseudo-V1 payload to canonical V0 payload
- `_ts` is generated in UTC at runtime
- `desk_snapshot` absence now returns a warning path for timer-only dry-run
- targeted tests added for timer payload and non-blocking snapshot absence

## Non-changes

- no `/etc/systemd/system` file modified
- no repo systemd file modified
- no manual service start added

## RISKS

- À qualifier.
