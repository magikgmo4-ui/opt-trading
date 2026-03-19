# Student Master Index

This file links the full `student` documentation set across the historical repo docs and the consolidated canonical project docs.

## Read First

- canonical project root: `/opt/trading/student`
- navigation entrypoint: `/opt/trading/student/INDEX.md`
- operator runbook: `/opt/trading/student/docs/RUNBOOK.md`
- quick reference: `/opt/trading/student/docs/QUICK_REFERENCE.md`

## Canonical Documentation

### Core

- `/opt/trading/student/README.md`
- `/opt/trading/student/INDEX.md`
- `/opt/trading/student/docs/ARCHITECTURE.md`
- `/opt/trading/student/docs/RUNBOOK.md`
- `/opt/trading/student/docs/QUICK_REFERENCE.md`

### Migration And Cleanup

- `/opt/trading/student/docs/PHASE2_MIGRATION.md`
- `/opt/trading/student/docs/DUPLICATES_AUDIT.md`
- `/opt/trading/student/docs/LEGACY_CALLERS_INVENTORY.md`
- `/opt/trading/student/docs/CONSOLIDATION_BEFORE_AFTER.md`
- `/opt/trading/student/scripts/legacy/migration_map.md`

### Delivery And Governance

- `/opt/trading/student/docs/DELIVERY_CHECKLIST.md`
- `/opt/trading/student/docs/GIT_PR_HANDOFF.md`
- `/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION.md`
- `/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION_SHORT.md`
- `/opt/trading/student/docs/PR_STUDENT_CONSOLIDATION_MANAGER.md`
- `/opt/trading/student/docs/references/kanban_references.md`

### Planning

- `/opt/trading/student/exports/kanban/KANBAN.md`
- `/opt/trading/student/exports/kanban/KANBAN_MANAGER.md`
- `/opt/trading/student/docs/MAINTENANCE_KANBAN.md`

## Historical Documentation In `/opt/trading/docs`

### DeepSeek Student

- `/opt/trading/docs/student_deepseek_runbook.md`
- `/opt/trading/docs/student_deepseek_quick_reference.md`

### Desk Pro Student

- `/opt/trading/docs/student_desk_pro_runbook.md`
- `/opt/trading/docs/student_desk_pro_quick_reference.md`

## Which One Should I Use?

- use `/opt/trading/student/docs/RUNBOOK.md` for current canonical operator flow
- use `/opt/trading/student/docs/QUICK_REFERENCE.md` for current canonical commands
- use `/opt/trading/docs/student_deepseek_runbook.md` only for historical DeepSeek Student behavior and old wrapper context
- use `/opt/trading/docs/student_desk_pro_runbook.md` only for the Desk Pro student role

## Command Model Today

- official global shortcuts:
  - `menu-student`
  - `cmd-student`
  - `sanity-student`
- canonical facade paths:
  - `/opt/trading/student/scripts/student_menu.sh`
  - `/opt/trading/student/scripts/student_cmd.sh`
  - `/opt/trading/student/scripts/student_sanity_check.sh`

## Notes

- the old docs remain useful as history and compatibility references
- the canonical source of truth is now the consolidated `/opt/trading/student` tree
