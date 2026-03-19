# Consolidation Before / After

## Before

- no single canonical `student` project root
- `student` logic split across:
  - `/opt/trading/modules/deepseek_hub/scripts/`
  - `/opt/trading/modules/deepseek_student/scripts/`
  - `/opt/trading/scripts/student/`
  - global shortcuts in `/usr/local/bin`
  - historical packs and audits in `/home/student/`
- global `student` shortcuts had already drifted historically and were repaired ad hoc
- installer logic existed in multiple places with overlapping responsibilities
- wrapper scripts still referenced legacy module paths directly

## After

- canonical root created: `/opt/trading/student`
- canonical top-level facades created:
  - `/opt/trading/student/scripts/student_cmd.sh`
  - `/opt/trading/student/scripts/student_menu.sh`
  - `/opt/trading/student/scripts/student_sanity_check.sh`
- global shortcuts now point to canonical student facades:
  - `/usr/local/bin/cmd-student`
  - `/usr/local/bin/menu-student`
  - `/usr/local/bin/sanity-student`
- deepseek hub and deepseek student assets copied under the consolidated tree
- migration, duplicates, and legacy caller audits documented inside the project
- canonical installer now lives at `/opt/trading/student/bin/install_shortcuts.sh`
- wrapper pathing updated to use the canonical student tree

## What Changed Structurally

### New canonical project areas

- `/opt/trading/student/README.md`
- `/opt/trading/student/INDEX.md`
- `/opt/trading/student/docs/`
- `/opt/trading/student/bin/`
- `/opt/trading/student/scripts/`
- `/opt/trading/student/exports/kanban/`

### New governance and migration docs

- `/opt/trading/student/docs/PHASE2_MIGRATION.md`
- `/opt/trading/student/docs/DUPLICATES_AUDIT.md`
- `/opt/trading/student/docs/LEGACY_CALLERS_INVENTORY.md`
- `/opt/trading/student/docs/CONSOLIDATION_BEFORE_AFTER.md`

## Current Official Rules

1. project root for `student`: `/opt/trading/student`
2. official installer: `/opt/trading/student/bin/install_shortcuts.sh`
3. official global shortcuts:
   - `cmd-student`
   - `menu-student`
   - `sanity-student`
4. official top-level runtime facades:
   - `/opt/trading/student/scripts/student_cmd.sh`
   - `/opt/trading/student/scripts/student_menu.sh`
   - `/opt/trading/student/scripts/student_sanity_check.sh`

## Remaining Debt

- duplicated command layers still exist between `deepseek_student` and `wrappers`
- historical docs still reference legacy module paths for traceability
- old source trees are still present and intentionally not deleted yet

## Validation Snapshot

- canonical facades tested successfully
- `sanity-student` passes from the canonical root
- canonical shortcuts for `student`, `deepseek_hub`, and `deepseek_student` were reinstalled successfully
