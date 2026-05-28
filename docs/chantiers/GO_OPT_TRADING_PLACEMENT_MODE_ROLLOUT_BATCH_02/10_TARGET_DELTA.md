---
go_id: GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02
doc_type: TARGET_DELTA
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 10_TARGET_DELTA

## Applied decisions

### `shared_sshfs_permanent`

- keep `machine_target: any`
- add `placement_mode: cross_host_facade`

Reason:
The module is a Linux client mount surface spanning a local machine and a remote source hosted on `admin-trading`. The cross-host nature is clear, but a single dominant local anchor is not stable enough to force a replacement of `any` in this GO.

### `shared`

- change `machine_target` from `any` to `admin_trading`
- add `placement_mode: cross_host_facade`

Reason:
The canonical source of truth for the surface is explicitly `admin-trading` (`/srv/sftp/shared_files/shared`, alias `/shared`), even if UX exists on multiple machines.

### `reseau_ssh`

- change `machine_target` from `any` to `admin_trading`
- add `placement_mode: cross_host_facade`

Reason:
The module is the canonical facade for multi-host SSH/network operations, but the orchestration/control reading is strongest on `admin_trading`.

### `mimo_open_observer`

- keep `machine_target: any`
- keep no `placement_mode` for now
- keep in deferred allowlist

Reason:
The repo still carries mixed signals (`active` module surface, scheduler/systemd wiring, historical docs marking it closed/student). This GO does not force a false precision.
