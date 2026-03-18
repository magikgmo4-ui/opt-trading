# Duplicates Audit

This audit focuses on overlap between `deepseek_hub`, `deepseek_student`, and `wrappers` inside `/opt/trading/student`.

## Findings

### 1. Command Layer Overlap

- canonical facade: `/opt/trading/student/scripts/student_cmd.sh`
- hub runtime command: `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_cmd.sh`
- student helper command: `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`
- compatibility wrapper command: `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`

Assessment:

- `student_cmd.sh` is intentionally thin and should stay
- `deepseek_hub_cmd.sh` is the main operational engine today
- `deepseek_student/deepseek_student_cmd.sh` is a focused helper for `sanity`, `pull`, `test`, `roadmap`
- `wrappers/deepseek_student_cmd.sh` is a richer operator wrapper with status, timers, summary, roadmap helpers

Conclusion:

- there is functional overlap between `deepseek_student/deepseek_student_cmd.sh` and `wrappers/deepseek_student_cmd.sh`
- they should not both remain as peer primary entrypoints long term

Recommendation:

- keep `student_cmd.sh` as the only official facade
- keep `deepseek_hub_cmd.sh` as the internal engine
- keep `wrappers/deepseek_student_cmd.sh` as the surviving module-level operator convenience command
- classify `deepseek_student/deepseek_student_cmd.sh` as a narrow helper implementation used for focused module actions only

Decision:

- survivor for interactive module-level usage: `/opt/trading/student/scripts/wrappers/deepseek_student_cmd.sh`
- retained helper backend: `/opt/trading/student/scripts/deepseek_student/deepseek_student_cmd.sh`

### 2. Shortcut Installer Overlap

- `/opt/trading/student/bin/install_shortcuts.sh`
- `/opt/trading/student/scripts/deepseek_hub/install_shortcuts.sh`
- `/opt/trading/student/scripts/deepseek_student/install_shortcuts.sh`

Assessment:

- three installers exist with overlapping purpose
- only `bin/install_shortcuts.sh` matches the new canonical root cleanly

Recommendation:

- keep `/opt/trading/student/bin/install_shortcuts.sh` as the single official installer
- treat the two module installers as legacy/internal until refactored or retired

### 3. Sanity Layer Overlap

- `/opt/trading/student/scripts/student_sanity_check.sh`
- `/opt/trading/student/scripts/deepseek_hub/sanity_check_deepseek_hub.sh`
- `/opt/trading/student/scripts/deepseek_student/sanity_check.sh`
- `/opt/trading/student/scripts/deepseek_student/sanity_check_deepseek_student.sh`
- `/opt/trading/student/scripts/wrappers/deepseek_student_sanity_check.sh`

Assessment:

- multiple sanity layers exist for different scopes
- this is acceptable short term, but naming is crowded and potentially confusing

Recommendation:

- keep `student_sanity_check.sh` as the only top-level official sanity command
- document the others as internal or scoped checks

### 4. Menu Layer Overlap

- `/opt/trading/student/scripts/student_menu.sh`
- `/opt/trading/student/scripts/deepseek_hub/deepseek_hub_menu.sh`
- `/opt/trading/student/scripts/deepseek_student/menu.sh`
- `/opt/trading/student/scripts/wrappers/deepseek_student_menu.sh`
- `/opt/trading/student/scripts/wrappers/desk_pro_student_menu.sh`

Assessment:

- `student_menu.sh` currently delegates to the hub menu
- `deepseek_student/menu.sh` is more of a module wrapper menu
- wrapper menus remain valid but should not be mistaken for root entrypoints

Recommendation:

- keep one official top-level menu only
- reclassify wrapper menus by purpose in docs

## Priority Cleanup Targets

1. normalize installer ownership around `/opt/trading/student/bin/install_shortcuts.sh`
2. decide whether `wrappers/deepseek_student_cmd.sh` or `deepseek_student/deepseek_student_cmd.sh` survives as the module-level command
3. document menu and sanity scopes so users stop calling the wrong layer
