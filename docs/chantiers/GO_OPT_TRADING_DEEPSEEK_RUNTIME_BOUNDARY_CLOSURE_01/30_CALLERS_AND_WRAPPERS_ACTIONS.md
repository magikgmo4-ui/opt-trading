---
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_BOUNDARY_CLOSURE_01
doc_type: CALLERS_AND_WRAPPERS_ACTIONS
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 30_CALLERS_AND_WRAPPERS_ACTIONS

## Required next execution checks

1. verify all active shortcuts that still land in `scripts/student/`
2. verify `post_change.sh` and any SSH/operator flows still depending on legacy wrappers
3. verify whether wrapper parity between `student/scripts/wrappers/` and `scripts/student/` is still required
4. confirm whether `cmd-deepseek_student` should resolve to student-side wrappers only

## Minimal action classification

- `student/scripts/` = keep and treat as canonical
- `scripts/student/` = keep temporarily, compat-only, audit before archive
- `modules/deepseek_student/` = no runtime promotion; later absorb, archive, or keep as non-runtime scaffold

## Follow-up execution GO

Recommended next implementation lot:

- `GO_OPT_TRADING_DEEPSEEK_RUNTIME_COMPAT_WRAPPERS_CLEANUP_01`

## Registry consequence after cleanup

Only after compat cleanup should a later GO decide whether:

- no central `deepseek_student` entry is needed,
- a central `legacy` entry remains useful,
- or a bounded `transitional` entry is justified.
