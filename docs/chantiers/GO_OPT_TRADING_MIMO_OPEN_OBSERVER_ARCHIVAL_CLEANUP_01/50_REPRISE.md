---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 50_REPRISE

## Summary

- `mimo_open_observer` is no longer exposed as a default active runtime line
- archive evidence, code, fixtures, and historical data are preserved
- runtime/scheduler/wrapper surfaces are now explicitly archival or opt-in legacy
- the next logical step is a dedicated allowlist-retirement registry GO

## Files touched

- `modules/mimo_open_observer/README.md`
- `modules/mimo_open_observer/LEGACY.md`
- `modules/mimo_open_observer/cmd.sh`
- `modules/mimo_open_observer/menu.sh`
- `modules/mimo_open_observer/sanity.sh`
- `modules/mimo_open_observer/scripts/mimo_open_observer_gate_replay.sh`
- `modules/mimo_open_observer/scripts/install_shortcuts.sh`
- `modules/mimo_open_observer/systemd/mimo_open_observer_gate_replay.service`
- `modules/mimo_open_observer/systemd/mimo_open_observer_gate_replay.timer`

## Resume point

```text
CURRENT_GO = GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01
MODE = bounded archival cleanup
STATUS = PR_OPENED_OR_READY

NEXT_IF_PASS:
GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
```

## Verdict

`PASS`
