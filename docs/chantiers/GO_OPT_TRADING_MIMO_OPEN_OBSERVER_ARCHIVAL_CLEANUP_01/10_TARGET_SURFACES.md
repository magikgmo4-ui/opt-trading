---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_ARCHIVAL_CLEANUP_01
doc_type: TARGET_SURFACES
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 10_TARGET_SURFACES

## Surfaces kept as archive evidence

- `modules/mimo_open_observer/app/`
- `modules/mimo_open_observer/docs/`
- `modules/mimo_open_observer/fixtures/`
- `modules/mimo_open_observer/data/`
- `modules/mimo_open_observer/systemd/`
- `modules/mimo_open_observer/registry_patch/`

## Surfaces neutralized from active default behavior

- `modules/mimo_open_observer/cmd.sh`
- `modules/mimo_open_observer/menu.sh`
- `modules/mimo_open_observer/sanity.sh`
- `modules/mimo_open_observer/scripts/mimo_open_observer_gate_replay.sh`
- `modules/mimo_open_observer/scripts/install_shortcuts.sh`

## Bounded cleanup rule

No asset is blindly deleted in this GO.

The cleanup converts the runtime-facing surfaces into explicit archival or opt-in legacy behavior, while keeping evidence and implementation files readable.
