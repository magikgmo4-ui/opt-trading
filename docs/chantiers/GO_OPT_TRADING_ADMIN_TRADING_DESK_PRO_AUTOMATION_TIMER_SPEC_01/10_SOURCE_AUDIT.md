---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01_SOURCE_AUDIT
doc_type: source_audit
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_SPEC_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 10_SOURCE_AUDIT - Timer/Systemd Patterns

## Existing timers

| Timer | Pattern | Usage |
| --- | --- | --- |
| `desk_retention.timer` | `OnBootSec=3min`, `OnUnitActiveSec=10min` | Type=oneshot, every 10min |
| `mimo_open_observer_gate_replay.timer` | `OnCalendar=Sun,Mon,Tue,Wed,Thu *-*-* 18:00:00` | Type=oneshot, daily market open |
| `bot-vision-headless-capture.timer` | periodic | headless visual capture |
| `bot_vision_step2_prune.timer` | periodic | visual data pruning |
| `bot_vision_step2_send.timer` | periodic | visual data dispatch |

## Pattern analysis

### Type=oneshot (common)

```ini
[Service]
Type=oneshot
ExecStart=/path/to/script.sh
```

### Timer configs

- `OnBootSec` — delai apres boot
- `OnUnitActiveSec` — intervalle periodique
- `OnCalendar` — schedule specifique (jour/semaine/heure)
- `AccuracySec` — precision
- `Persistent` — catch-up si machine eteinte

## Desk Pro context

- Dry-run module: `modules/desk_pro/dry_run.py`
- Execution: read-only, pas d'action live
- Gate: `no_trade`, `no_telegram`, `no_webhook`, `no_systemd`
- Frequency recommandee: periodique read-only

## Audit conclusion

- Les timers existants sont bien documentes
- Pattern `Type=oneshot` avec timer externe est standard
- Desk Pro timer doit suivre le meme pattern
- spec suivante: timer pour dry-run periodique