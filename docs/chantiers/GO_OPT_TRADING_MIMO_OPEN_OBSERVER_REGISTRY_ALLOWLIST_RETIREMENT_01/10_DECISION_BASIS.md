---
go_id: GO_OPT_TRADING_MIMO_OPEN_OBSERVER_REGISTRY_ALLOWLIST_RETIREMENT_01
doc_type: DECISION_BASIS
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-29
---

# 10_DECISION_BASIS

## What changed since the allowlist exception

The earlier allowlist existed because:

- runtime signals were mixed
- strategic docs said `CLOSED (student)`
- registry semantics were too ambiguous to force a target

The archival cleanup now makes the state sufficiently clear:

- runtime surfaces are blocked by default
- scheduler and wrappers are preserved only as archive residue
- the module is explicitly documented as a student-side archival residue

## Registry implication

The module no longer needs `machine_target:any` as a hedge against ambiguity.

Its dominant anchor is now the student-side surface that survives only as bounded archival residue.
