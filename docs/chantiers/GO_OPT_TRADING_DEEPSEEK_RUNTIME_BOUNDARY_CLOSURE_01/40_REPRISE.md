---
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 40_REPRISE

## Summary

- `student/scripts/` is confirmed as the surviving canonical runtime surface
- `scripts/student/` is confirmed as legacy compatibility only
- `modules/deepseek_student/` is confirmed as non-runtime scaffold, not runtime owner
- the boundary question is now closed at the decision level; what remains is compat-wrapper cleanup and caller verification

## Files created

- `docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01/00_INITIAL_PROJECT_DOC.md`
- `10_SURFACE_AUDIT.md`
- `20_BOUNDARY_DECISION.md`
- `30_CALLERS_AND_WRAPPERS_ACTIONS.md`
- `40_REPRISE.md`

## Diff summary

- closes the runtime-boundary ambiguity between the three `deepseek_student` surfaces
- fixes the canonical survivor as `student/scripts/`
- defers only the compat cleanup and shortcut migration work

## Verification

```bash
rg -n "student/scripts|scripts/student|modules/deepseek_student|compat|runtime owner" docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01
git status --short --branch
git diff -- docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01
```

## Verdict

`PASS`
