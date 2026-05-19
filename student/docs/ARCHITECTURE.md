# Student Architecture

This folder is the canonical target for consolidating the `student` project.

Core layers:

- `scripts/student_*`: stable top-level operator entrypoints
- `scripts/deepseek_hub/`: hub runtime commands and menu
- `scripts/deepseek_student/`: backend helper tooling for focused DeepSeek student actions
- `scripts/wrappers/`: official `deepseek_student` operator facade layer
- `exports/kanban/`: planning and tracking artifacts

Facade rules:

- top-level official workspace facade:
  - `scripts/student_cmd.sh`
  - `scripts/student_menu.sh`
  - `scripts/student_sanity_check.sh`
- module-level official `deepseek_student` facade:
  - `scripts/wrappers/deepseek_student_cmd.sh`
  - `scripts/wrappers/deepseek_student_menu.sh`
  - `scripts/wrappers/deepseek_student_sanity_check.sh`
- `scripts/deepseek_student/` remains available as backend/helper scope, not as the preferred operator entrypoint

Migration note:

Legacy scripts still exist under `/opt/trading/modules/*` and `/opt/trading/scripts/student/`.

Canonical root decision:

- use `/opt/trading/student` as the single project root for the `student` workspace
- use `scripts/student_*` as the only stable top-level entrypoints
- treat `/opt/trading/modules/deepseek_hub/scripts/`, `/opt/trading/modules/deepseek_student/scripts/`, and `/opt/trading/scripts/student/` as upstream legacy sources until cleanup is complete
