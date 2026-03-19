# PR Student Consolidation Short

## Title

`student: consolidate canonical workspace`

## Summary

- consolidate the `student` workspace under `/opt/trading/student`
- repoint canonical shortcuts and wrapper paths to the new root
- add a master index plus migration, audit, and planning documentation for the transition

## Validation

- `sanity-student` passes from the canonical root
- canonical shortcut installation verified for `student`, `deepseek_hub`, and `deepseek_student`
- rewired `deepseek_student_run_logged.sh status` succeeds

## Base

- base: `sot/mainline`
- head: `student`
