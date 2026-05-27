---
go_id: GO_OPT_TRADING_DEEPSEEK_RUNTIME_COMPAT_WRAPPERS_CLEANUP_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-27
---

# 40_REPRISE

## Summary

- `scripts/student/` now behaves as a compatibility shim layer toward `student/scripts/`
- the recursive `scripts/student/student_cmd.sh` bug is removed
- root shortcut installation now points directly to canonical `student/scripts/` entrypoints
- the legacy directory is still present, but no longer carries the primary behavior for the covered entrypoints

## Files touched

- `scripts/student/student_cmd.sh`
- `scripts/student/student_menu.sh`
- `scripts/student/student_sanity_check.sh`
- `scripts/student/deepseek_student_cmd.sh`
- `scripts/student/deepseek_student_menu.sh`
- `scripts/student/deepseek_student_sanity_check.sh`
- `scripts/student/deepseek_student_install.sh`
- `scripts/install_student_shortcuts.sh`
- `tests/governance/test_deepseek_runtime_compat_wrappers.py`

## Verification

```bash
python3 -m pytest tests/governance/test_deepseek_runtime_compat_wrappers.py
git diff --check
git status --short --branch
```

## Verdict

`PASS`
