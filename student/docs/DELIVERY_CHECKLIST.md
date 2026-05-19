# Delivery Checklist

## Canonical Structure

- [x] `student` root exists at `/opt/trading/student`
- [x] top-level facades exist in `/opt/trading/student/scripts/`
- [x] installer scripts exist in `/opt/trading/student/bin/`
- [x] governance and migration docs exist in `/opt/trading/student/docs/`

## Shortcuts

- [x] `menu-student` points to `/opt/trading/student/scripts/student_menu.sh`
- [x] `cmd-student` points to `/opt/trading/student/scripts/student_cmd.sh`
- [x] `sanity-student` points to `/opt/trading/student/scripts/student_sanity_check.sh`
- [x] canonical shortcuts for `deepseek_hub` and `deepseek_student` are installable

## Runtime Validation

- [x] `sanity-student`
- [x] `cmd-student status`
- [x] `cmd-deepseek_student sanity`
- [x] menu smoke test completed earlier for `menu-student`

## Documentation

- [x] architecture doc
- [x] runbook
- [x] quick reference
- [x] migration plan
- [x] duplicate audit
- [x] legacy callers inventory
- [x] before/after report
- [x] PR text variants
- [x] Git/PR handoff doc

## Git State

- [x] branch in use: `student`
- [x] consolidation commits created locally
- [ ] branch pushed to remote
- [ ] pull request opened

## Known Constraints

- [x] unrelated pre-existing repo changes outside `student/` were left untouched
- [x] legacy source trees are still present for compatibility
- [x] GitHub push remains blocked on this machine without auth
