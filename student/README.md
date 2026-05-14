# Student Project

Canonical workspace for the `student` operator experience inside `/opt/trading`.

Scope:

- global `student` shortcuts
- DeepSeek hub operator entrypoints
- DeepSeek student helper scripts
- student-facing wrappers and documentation
- migration artifacts used to converge legacy layouts

Main entrypoints:

- `scripts/student_cmd.sh`
- `scripts/student_menu.sh`
- `scripts/student_sanity_check.sh`

Supporting areas:

- `scripts/deepseek_hub/`
- `scripts/deepseek_student/`
- `scripts/wrappers/`
- `docs/`
- `exports/kanban/`

Documentation entrypoints:

- master index: `/opt/trading/student/docs/MASTER_INDEX.md`
- operator index: `/opt/trading/student/INDEX.md`

This tree is created as a consolidation target. Existing legacy locations remain in place until migration is validated.

Canonical decision:

- official project root for `student`: `/opt/trading/student`
- official global shortcuts:
  - `menu-student` -> `/opt/trading/student/scripts/student_menu.sh`
  - `cmd-student` -> `/opt/trading/student/scripts/student_cmd.sh`
  - `sanity-student` -> `/opt/trading/student/scripts/student_sanity_check.sh`

Legacy locations are now compatibility sources only and should not be used as primary entrypoints.

## Migration status

See `scripts/MIGRATION_STATUS.md` for the current DeepSeek consolidation state.
The `scripts/student/` legacy directory is preserved for backward compatibility
with `post_change.sh` and `deepseek_hub` callers.
