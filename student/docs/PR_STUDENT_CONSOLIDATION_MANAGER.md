# PR Student Consolidation Manager

## Title

`student: consolidate canonical workspace`

## Impact

- gives `student` a single official root at `/opt/trading/student`
- reduces path drift and shortcut inconsistency across the operator toolchain
- makes future maintenance easier by separating canonical entrypoints from legacy sources
- adds a master documentation index plus migration and audit artifacts so cleanup can continue without losing traceability

## Business / Ops Value

- lower operator confusion around which `student` command path is authoritative
- faster onboarding through one navigation point and one install path
- safer evolution because legacy areas are documented before removal
- better planning visibility through embedded Kanban and transition documents

## Technical Outcome

- canonical facades now front the workspace
- global shortcuts point to the consolidated root
- wrapper pathing is aligned with the canonical tree
- command ownership is documented, including the surviving `deepseek_student_cmd` layer

## Risk Notes

- legacy source trees remain present during the transition by design
- unrelated pre-existing repo changes are not part of this consolidation

## Recommended Review Angle

- validate that `/opt/trading/student` is the correct long-term root
- validate that shortcut ownership is now clear enough for operators
- confirm the phase 2 migration plan before deleting any legacy paths
