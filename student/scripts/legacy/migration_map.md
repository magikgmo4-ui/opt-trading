# Legacy Migration Map

Legacy sources currently in use:

- `/opt/trading/modules/deepseek_hub/scripts/`
- `/opt/trading/modules/deepseek_student/scripts/`
- `/opt/trading/scripts/student/`

Canonical target:

- `/opt/trading/student/`

Strategy:

1. Copy first
2. Validate canonical entrypoints
3. Repoint shortcuts
4. Deprecate old paths gradually

Deprecated as primary entrypoints:

- `/opt/trading/modules/deepseek_hub/scripts/deepseek_hub_cmd.sh`
- `/opt/trading/modules/deepseek_hub/scripts/deepseek_hub_menu.sh`
- `/opt/trading/modules/deepseek_hub/scripts/sanity_check_deepseek_hub.sh`
- `/opt/trading/scripts/student/*`

Canonical replacements:

- `/opt/trading/student/scripts/student_cmd.sh`
- `/opt/trading/student/scripts/student_menu.sh`
- `/opt/trading/student/scripts/student_sanity_check.sh`
