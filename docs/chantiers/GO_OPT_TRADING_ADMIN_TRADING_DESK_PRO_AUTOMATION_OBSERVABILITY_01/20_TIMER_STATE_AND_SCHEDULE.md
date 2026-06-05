---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01_TIMER_STATE
doc_type: timer_state_and_schedule
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_OBSERVABILITY_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 20_TIMER_STATE_AND_SCHEDULE - Timer State and Schedule

## list-timers observation

```text
NEXT -
LEFT -
LAST -
PASSED -
UNIT desk_pro_dry_run.timer
ACTIVATES desk_pro_dry_run.service
```

## systemctl show observation

- `UnitFileState=enabled`
- `ActiveState=inactive`
- `SubState=dead`
- `Persistent=no`
- `Result=success`
- `NextElapseUSecMonotonic=infinity`
- `LastTriggerUSecMonotonic=0`
- `TimersMonotonic={ OnBootUSec=5min ; next_elapse=0 }`
- `TimersMonotonic={ OnUnitActiveUSec=15min ; next_elapse=0 }`

## Service execution observation

- `ExecMainPID=0`
- `ExecMainStatus=0`
- `ExecMainStartTimestampMonotonic=0`
- `ExecMainExitTimestampMonotonic=0`
- `ActiveState=inactive`
- `Result=success`

## Interpretation

- le timer est arme au niveau systemd via `enabled`
- aucun declenchement naturel n'est visible a ce stade
- aucun start manuel n'a ete effectue dans ce GO
- aucun prochain trigger calcule n'est affiche actuellement par systemd

## RISKS

- À qualifier.
