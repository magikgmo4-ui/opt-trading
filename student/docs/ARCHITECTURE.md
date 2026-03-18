# Student Architecture

This folder is the canonical target for consolidating the `student` project.

Core layers:

- `scripts/student_*`: stable top-level operator entrypoints
- `scripts/deepseek_hub/`: hub runtime commands and menu
- `scripts/deepseek_student/`: module-specific DeepSeek student tooling
- `scripts/wrappers/`: compatibility and operator convenience scripts
- `exports/kanban/`: planning and tracking artifacts

Migration note:

Legacy scripts still exist under `/opt/trading/modules/*` and `/opt/trading/scripts/student/`.

Canonical root decision:

- use `/opt/trading/student` as the single project root for the `student` workspace
- use `scripts/student_*` as the only stable top-level entrypoints
- treat `/opt/trading/modules/deepseek_hub/scripts/`, `/opt/trading/modules/deepseek_student/scripts/`, and `/opt/trading/scripts/student/` as upstream legacy sources until cleanup is complete
