# DeepSeek Student Scripts — Migration Status

## Canonical location

`student/scripts/` is the official operator workspace for the DeepSeek cluster.

## Current state (2026-05-13)

### Active — student/scripts/
```text
student/scripts/student_cmd.sh         → entrypoint unifié
student/scripts/student_menu.sh        → menu interactif
student/scripts/student_sanity_check.sh → validations
student/scripts/deepseek_hub/          → hub unifié (2 files)
student/scripts/deepseek_student/      → core étudiant (7 files)
student/scripts/wrappers/              → wrappers compat (18 files)
```

### Legacy — scripts/student/
```text
scripts/student/  → 22 files, legacy flat directory
```
**Do not delete.** Still referenced by:
- `scripts/post_change.sh` (cmd-deepseek_response, cmd-deepseek_thinced_refs)
- `modules/deepseek_student/README.md` (explicit "do not delete")
- `modules/deepseek_hub/README.md` (runtime truth)

## Migration decision

```text
Decision: keep both directories for backward compatibility.
No deletion of scripts/student/ at this stage.
Future migration: update shortcuts to point to student/scripts/,
then archive scripts/student/ after verification of all callers.
```

## Phase 1 — Callers audit (executed)

```text
- scripts/post_change.sh: SSH student calls cmd-deepseek_response + cmd-deepseek_thinking
- modules/deepseek_hub/scripts/deepseek_hub_cmd.sh: calls cmd-deepseek_student roadmap
- modules/deepseek_hub/scripts/sanity_check_deepseek_hub.sh: checks cmd-deepseek_*
- modules/repo_hygiene/: notes about cleaning up scripts/student/
```

## Phase 2 — Ready for manual migration

No automated migration in this GO. The operator should:
1. Verify that student/scripts/ shortcuts are installed
2. Test post_change workflow
3. Only then consider archiving scripts/student/
