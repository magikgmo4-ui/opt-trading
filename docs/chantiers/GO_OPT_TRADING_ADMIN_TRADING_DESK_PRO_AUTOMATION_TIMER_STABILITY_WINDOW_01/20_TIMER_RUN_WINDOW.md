---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01_RUN_WINDOW
doc_type: timer_run_window
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_STABILITY_WINDOW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-11
---

# 20_TIMER_RUN_WINDOW - Timer Run Window

## Post-fix natural runs observed

Runs after the first retained post-fix trigger `Sat 2026-05-09 06:59:23 EDT` include at least:

| Timestamp | Exit | Payload status | Errors | Warnings | Safety flags | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-05-09 06:59:23 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-09 07:14:23 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 09:30:14 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 09:45:14 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 10:00:15 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 10:15:15 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 10:30:15 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 10:45:15 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 11:00:16 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |
| 2026-05-11 11:15:16 EDT | 0/SUCCESS | WARN | [] | optional-only | all true | clean |

## Window result

- number of clean post-fix runs observed: `>= 10`
- minimum PASS threshold met: `YES`
- systemd failure or blocked state observed: `NO`
