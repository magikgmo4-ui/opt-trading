---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01_POSTSTART
doc_type: post_start_observation
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_START_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 30_POST_START_OBSERVATION - Post Start Observation

## Timer state after start

```text
Loaded: loaded (/etc/systemd/system/desk_pro_dry_run.timer; enabled; preset: enabled)
Active: active (waiting)
Trigger: Sat 2026-05-09 06:29:21 EDT
```

## Service state after start

```text
Loaded: loaded (/etc/systemd/system/desk_pro_dry_run.service; static)
Active: inactive (dead)
Process: ExecStart exited, status=0/SUCCESS
CPU: 95ms
```

## list-timers observation

```text
NEXT   Sat 2026-05-09 06:29:21 EDT
LEFT   14min left
LAST   Sat 2026-05-09 06:14:21 EDT
PASSED 8s ago
UNIT   desk_pro_dry_run.timer
```

## systemctl show highlights

- timer: `ActiveState=active`
- timer: `SubState=waiting`
- timer: `LastTriggerUSec=Sat 2026-05-09 06:14:21 EDT`
- service: `ExecMainStatus=0`
- service: `ExecMainPID=572417`
- service: `Result=success`

## Interpretation

- objectif principal atteint: timer active avec prochain trigger visible
- service ne reste pas actif apres execution
- aucun start manuel du service n'a ete fait

## RISKS

- À qualifier.
