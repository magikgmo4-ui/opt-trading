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

> **Phase 2 update — 2026-03-20** : items 1–4 of the priority rewiring list have been
> verified as already executed. The descriptions below are preserved as audit history.
> Current state column added.

### deepseek_hub installer copy

- `/opt/trading/student/scripts/deepseek_hub/install_shortcuts.sh`
  - **Was**: writing shortcuts to `$ROOT/modules/deepseek_hub/scripts/...`
  - **Current state**: CORRIGÉ — points to `$ROOT/scripts/deepseek_hub/...` with `$ROOT` defaulting to `/opt/trading/student`. Adds NOTE directing to `bin/install_shortcuts.sh` as canonical installer.

Assessment:

- no longer legacy-oriented at the symlink level
- still scoped to deepseek_hub shortcuts only; `bin/install_shortcuts.sh` remains the full-scope canonical installer
- retain as module-scoped convenience installer; do not use as primary

### deepseek_student installer copy

- `/opt/trading/student/scripts/deepseek_student/install_shortcuts.sh`
  - **Was**: writing shortcuts to `$ROOT/modules/deepseek_student/scripts/...`
  - **Current state**: CORRIGÉ — points to `$ROOT/scripts/wrappers/deepseek_student_*.sh`. Adds NOTE directing to `bin/install_shortcuts.sh`.

Assessment:

- no longer pointing to legacy module paths
- retain for traceability; canonical installer remains `bin/install_shortcuts.sh`

### wrapper command chain

- `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`
  - **Was**: computing `DEEPSEEK_HUB_CMD="$ROOT_DIR/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh"`
  - **Current state**: CORRIGÉ — uses `DEEPSEEK_HUB_CMD="$STUDENT_ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh"` resolved from script location.

- `/opt/trading/student/scripts/wrappers/deepseek_student_run_logged.sh`
  - **Was**: referring to `$ROOT_DIR/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh`
  - **Current state**: CORRIGÉ — uses `DEEPSEEK_HUB_CMD="$STUDENT_ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh"` resolved from script location.
  - **Remaining**: contains a PATH fallback injection for `cmd-deepseek_thinking` pointing to `$ROOT_DIR/modules/deepseek_thinking/scripts` and `$ROOT_DIR/modules/deepseek_response/scripts`. These are **legitimate external module dependencies** (`deepseek_thinking`, `deepseek_response`), not legacy student paths. Do not touch without a dedicated module dependency chantier.

## 3. Command Alias Dependence

- `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh`
  - calls `cmd-deepseek_student roadmap ...`
- `/opt/trading/student/scripts/deepseek_hub/sanity_check_deepseek_hub.sh`
  - checks presence of `cmd-deepseek_student`
- `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`
  - may fall back to `sanity-deepseek_student`

Assessment:

- these are not direct old path references, but they still depend on global command aliases rather than canonical in-tree paths
- medium-priority cleanup target — unchanged, deferred to future chantier

## 4. Priority Order For Rewiring — État 2026-03-20

| Item | Script | État |
|---|---|---|
| 1 | `wrappers/deepseek_student_cmd.sh` | CORRIGÉ |
| 2 | `wrappers/deepseek_student_run_logged.sh` | CORRIGÉ (sauf PATH externe légitime) |
| 3 | `scripts/deepseek_hub/install_shortcuts.sh` | CORRIGÉ |
| 4 | `scripts/deepseek_student/install_shortcuts.sh` | CORRIGÉ |
| 5 | alias-based fallback logic | EN ATTENTE — chantier futur |

## 5. Decision

- official installer: `/opt/trading/student/bin/install_shortcuts.sh`
- official facades:
  - `/opt/trading/student/scripts/student_cmd.sh`
  - `/opt/trading/student/scripts/student_menu.sh`
  - `/opt/trading/student/scripts/student_sanity_check.sh`
- official internal engine:
  - `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh`
