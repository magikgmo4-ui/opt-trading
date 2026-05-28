---
go_id: GO_OPT_TRADING_PLACEMENT_MODE_ROLLOUT_BATCH_02
doc_type: TEST_AND_ALLOWLIST_CHANGES
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-28
---

# 30_TEST_AND_ALLOWLIST_CHANGES

## Governance tightening

`tests/governance/test_machine_target_model_impl.py` is tightened so that the deferred allowlist shrinks from four entries to one.

## Residual allowlist after this GO

- `mimo_open_observer`

## Why not zero immediately

The repo still exposes contradictory state signals for `mimo_open_observer` across runtime, scheduler wiring, and historical closeout docs. Keeping one explicit residual exception is safer than encoding a fabricated anchor.
