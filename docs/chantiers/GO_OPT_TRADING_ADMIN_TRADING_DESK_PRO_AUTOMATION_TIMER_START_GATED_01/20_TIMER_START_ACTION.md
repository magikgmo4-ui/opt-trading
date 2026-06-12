---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01_ACTION
doc_type: timer_start_action
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 20_TIMER_START_ACTION - Timer Start Action

## Authorized action executed

```bash
sudo systemctl start desk_pro_dry_run.timer
```

## Forbidden action not executed

```bash
sudo systemctl start desk_pro_dry_run.service
```

## Immediate effect observed

- timer passe a `active (waiting)`
- next trigger devient visible
- systemd a aussi declenche immediatement un run du service relie
- ce run n'a pas ete un start manuel du service, mais un effet de bord systemd du start du timer sur cet hote

## Safety interpretation

- timer start: YES
- manual service start: NO
- trade: NO
- webhook: NO
- Telegram: NO

## RISKS

- À qualifier.
