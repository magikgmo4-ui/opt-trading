---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_STATE_CLARIFICATION_01
doc_type: PLACEMENT_MODE_DECISION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 30_PLACEMENT_MODE_DECISION

## Decision

Do not assign `placement_mode` yet.

Keep `mimo_open_observer` in the residual allowlist for now.

## Why not `portable_tool`

The module is not a generic portable helper.

It has:

- explicit student-side historical classification
- scheduler/systemd packaging
- market-window specific runtime behavior

So `portable_tool` would understate its runtime specificity.

## Why not `single_host`

The strongest machine hint is `student`, but the current canonical evidence is still indirect and historically conflicting rather than explicitly normalized in the registry model.

## Why not `cross_host_facade`

The module is not primarily a cross-host facade. It is a self-contained observer pipeline with local scheduling behavior.

## Why not `compatibility_shim`

It is not a compat alias like the DeepSeek student shims.

## Current conclusion

The correct near-term action is not a forced `placement_mode` realignment.

It is first a state/closure decision on whether this module should:

1. be kept as a real student-anchored runnable module,
2. or be archived/retired as historical residue.
