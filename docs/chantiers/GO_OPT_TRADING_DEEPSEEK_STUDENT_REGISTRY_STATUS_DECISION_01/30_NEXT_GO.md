---
go_id: GO_OPT_TRADING_DEEPSEEK_STUDENT_REGISTRY_STATUS_DECISION_01
doc_type: NEXT_GO
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 30_NEXT_GO

## Next execution GO

Recommended next GO:

- `GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01`

## Target of that GO

1. decide the surviving physical/runtime surface among:
- `modules/deepseek_student/`
- `scripts/student/`
- `student/scripts/`

2. verify remaining callers and compat wrappers

3. determine whether the surviving object should later enter central registry as:
- no entry at all,
- `legacy`,
- or `transitional`

## Only after that

A follow-up registry lot may safely do one of these:

1. add a central `legacy` entry if the surviving object is purely compatibility-facing
2. add a central `transitional` entry if a bounded migration surface remains intentionally exposed
3. confirm permanent exclusion if `deepseek_student` is fully absorbed or archived
