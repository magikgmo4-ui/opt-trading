---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01
doc_type: DECISION
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 20_DECISION

## Final decision

`deepseek_student` must remain outside central registries for now.

The physical/runtime closure must precede any central registry entry.

## Why not `legacy` now

Adding central `legacy` immediately would still imply that `modules/deepseek_student/` is the right object to register centrally.

Current evidence says the opposite:

- the module path is not the runtime truth
- the canonical operator workspace is `student/scripts/`
- the legacy directory `scripts/student/` is still active for compatibility
- some surfaces already mark `deepseek_student` as closed or archived

So the problem is not only vocabulary. It is first a boundary problem.

## Why not `transitional` now

`transitional` would better match the migration narrative than `legacy`, but it still centralizes an unstable object before the runtime boundary is closed.

That would risk legitimizing a temporary module path as a canonical central entry.

## Canonical rule set from this GO

1. `deepseek_student` stays out of `registry/modules_registry.yaml` in the current state.
2. no wrapper or UI central entry is added for it in this lot.
3. family/product docs may continue to describe limited or transitional usability as long as they do not claim central registry ownership.
4. the next execution lot must close or explicitly normalize the physical/runtime boundary first.
