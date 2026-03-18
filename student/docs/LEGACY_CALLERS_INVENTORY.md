# Legacy Callers Inventory

This inventory captures the main legacy-style references still present inside `/opt/trading/student` after consolidation.

## 1. Legacy Path References In Documentation

- `/opt/trading/student/docs/ARCHITECTURE.md`
  - references `/opt/trading/modules/*` and `/opt/trading/scripts/student/` as legacy sources
- `/opt/trading/student/docs/PHASE2_MIGRATION.md`
  - lists legacy source folders and first replacement candidates
- `/opt/trading/student/scripts/legacy/migration_map.md`
  - records deprecated primary entrypoints
- `/opt/trading/student/docs/references/kanban_references.md`
  - keeps original historical references used to build the Kanban
- `/opt/trading/student/exports/kanban/KANBAN.md`
- `/opt/trading/student/exports/kanban/KANBAN_MANAGER.md`
  - still mention legacy module paths because they preserve the evidence used during planning

Assessment:

- these references are acceptable because they are documentation, not runtime callers
- they should remain until the historical trail is no longer needed

## 2. Runtime Scripts Still Pointing To Legacy-Oriented Targets

### deepseek_hub installer copy

- `/opt/trading/student/scripts/deepseek_hub/install_shortcuts.sh`
  - still writes shortcuts to `$ROOT/modules/deepseek_hub/scripts/...`

Assessment:

- this is now legacy-oriented inside the consolidated tree
- canonical installer should be `/opt/trading/student/bin/install_shortcuts.sh`

### deepseek_student installer copy

- `/opt/trading/student/scripts/deepseek_student/install_shortcuts.sh`
  - still writes shortcuts to `$ROOT/modules/deepseek_student/scripts/...`

Assessment:

- same issue as above
- keep for traceability, but do not use as the official installer

### wrapper command chain

- `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`
  - computes `DEEPSEEK_HUB_CMD="$ROOT_DIR/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh"`
- `/opt/trading/student/scripts/wrappers/deepseek_student_run_logged.sh`
  - also refers to `$ROOT_DIR/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh`

Assessment:

- these are the main runtime callers still using legacy-style module paths
- they are priority candidates for phase 2 rewiring to `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh`

## 3. Command Alias Dependence

- `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh`
  - calls `cmd-deepseek_student roadmap ...`
- `/opt/trading/student/scripts/deepseek_hub/sanity_check_deepseek_hub.sh`
  - checks presence of `cmd-deepseek_student`
- `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`
  - may fall back to `sanity-deepseek_student`

Assessment:

- these are not direct old path references, but they still depend on global command aliases rather than canonical in-tree paths
- medium-priority cleanup target

## 4. Priority Order For Rewiring

1. `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`
2. `/opt/trading/student/scripts/wrappers/deepseek_student_run_logged.sh`
3. `/opt/trading/student/scripts/deepseek_hub/install_shortcuts.sh`
4. `/opt/trading/student/scripts/deepseek_student/install_shortcuts.sh`
5. alias-based fallback logic in hub and deepseek_student scripts

## 5. Decision

- official installer: `/opt/trading/student/bin/install_shortcuts.sh`
- official facades:
  - `/opt/trading/student/scripts/student_cmd.sh`
  - `/opt/trading/student/scripts/student_menu.sh`
  - `/opt/trading/student/scripts/student_sanity_check.sh`
- official internal engine:
  - `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh`
