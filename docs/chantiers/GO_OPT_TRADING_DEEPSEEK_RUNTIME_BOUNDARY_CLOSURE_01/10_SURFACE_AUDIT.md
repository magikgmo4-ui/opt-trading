---
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01
doc_type: SURFACE_AUDIT
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 10_SURFACE_AUDIT

## Observed surfaces

### `student/scripts/`

- declared as the official operator workspace in `student/scripts/MIGRATION_STATUS.md`
- owns `student_cmd.sh`, `student_menu.sh`, `student_sanity_check.sh`
- contains `deepseek_hub/`, `deepseek_student/`, and `wrappers/`
- `student/scripts/student_cmd.sh` delegates to `student/scripts/deepseek_hub/deepseek_hub_cmd.sh`

### `scripts/student/`

- explicitly marked legacy in `student/scripts/MIGRATION_STATUS.md` and `scripts/student/LEGACY.md`
- still preserved for backward compatibility
- still carries wrapper commands and reporting helpers
- still referenced by product docs and migration docs

### `modules/deepseek_student/`

- README says it is not the current runtime truth
- README says active logic is in `scripts/student/` and canonical target is `student/scripts/`
- current scripts are a partial module surface, not the active runtime authority

## Callers and compat evidence

- `modules/deepseek_hub/scripts/deepseek_hub_cmd.sh` still calls `cmd-deepseek_student` for roadmap flows
- migration docs still require caller verification before archiving `scripts/student/`
- product docs still expose `deepseek_student` as bounded usable via student-side wrappers

## Boundary conclusion

The repo no longer has three equal candidates.

It has:

1. one canonical survivor candidate: `student/scripts/`
2. one bounded compatibility layer: `scripts/student/`
3. one non-runtime module scaffold: `modules/deepseek_student/`
