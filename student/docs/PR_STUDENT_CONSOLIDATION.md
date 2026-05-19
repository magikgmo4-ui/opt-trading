# PR Student Consolidation

## Title

`student: consolidate canonical workspace`

## Summary

- consolidate the `student` operator workspace under `/opt/trading/student`
- repoint canonical shortcuts and wrapper paths to the new consolidated root
- add migration, audit, before/after, and Kanban documentation to support the transition

## What Changed

- created the canonical project root at `/opt/trading/student`
- added stable top-level entrypoints:
  - `/opt/trading/student/scripts/student_cmd.sh`
  - `/opt/trading/student/scripts/student_menu.sh`
  - `/opt/trading/student/scripts/student_sanity_check.sh`
- repointed global shortcuts to the canonical `student` facades
- copied `deepseek_hub`, `deepseek_student`, and wrapper assets into the consolidated tree
- unified shortcut installation around `/opt/trading/student/bin/install_shortcuts.sh`
- rewired wrapper scripts to use canonical student paths instead of legacy module paths
- added governance and migration docs:
  - `MASTER_INDEX.md`
  - `INDEX.md`
  - `PHASE2_MIGRATION.md`
  - `DUPLICATES_AUDIT.md`
  - `LEGACY_CALLERS_INVENTORY.md`
  - `CONSOLIDATION_BEFORE_AFTER.md`

## Validation

- verified canonical facades under `/opt/trading/student/scripts/`
- verified `sanity-student` passes from the canonical root
- verified `deepseek_student_run_logged.sh status` succeeds after rewiring
- verified canonical shortcut installation for:
  - `student`
  - `deepseek_hub`
  - `deepseek_student`

## Notes

- legacy source trees remain in place intentionally for compatibility
- duplicate command layers are now documented, with `wrappers/deepseek_student_cmd.sh` designated as the surviving module-level operator command
- the repo still contains unrelated pre-existing changes outside the consolidated `student/` subtree

## Suggested Base

- base branch: `sot/mainline`
- head branch: `student`
