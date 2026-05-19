# Phase 2 Migration

This phase replaces legacy direct calls with canonical `student` facades without deleting upstream sources yet.

## Goal

Move callers from scattered legacy paths to:

- `/opt/trading/student/scripts/student_cmd.sh`
- `/opt/trading/student/scripts/student_menu.sh`
- `/opt/trading/student/scripts/student_sanity_check.sh`

## Legacy Sources Still Present

- `/opt/trading/modules/deepseek_hub/scripts/`
- `/opt/trading/modules/deepseek_student/scripts/`
- `/opt/trading/scripts/student/`

## Recommended Sequence

1. Inventory callers
   - search shell scripts, docs, timers, aliases, and desktop launchers for direct references to old paths
   - prioritize callers of `deepseek_hub_cmd.sh`, `deepseek_hub_menu.sh`, `sanity_check_deepseek_hub.sh`

2. Replace top-level operator calls first
   - replace direct `modules/deepseek_hub/scripts/*` invocations with `student/scripts/student_*`
   - replace user instructions in docs with canonical paths

3. Keep compatibility wrappers during transition
   - preserve old script locations while the new root stabilizes
   - do not delete `scripts/wrappers/` yet

4. Validate after each wave
   - run `sanity-student`
   - run `cmd-student status`
   - open `menu-student`

5. Deprecate old entrypoints explicitly
   - add deprecation notices in legacy wrappers where useful
   - move low-value legacy items to `legacy/` notes before removal

## First Candidates For Replacement — État 2026-03-20

> Vérification locale effectuée le 2026-03-20 dans le cadre de `GO_STUDENT_PHASE2_MIGRATION_01`.

| Candidat | État |
|---|---|
| Docs référençant `/opt/trading/modules/deepseek_hub/scripts/` | TOLÉRÉ — références documentaires uniquement. Acceptable comme mémoire historique. |
| Helper installers pointant vers les chemins modules | CORRIGÉ — `scripts/deepseek_hub/install_shortcuts.sh` et `scripts/deepseek_student/install_shortcuts.sh` pointent désormais vers les chemins canoniques `student/`. |
| Wrappers calculant `ROOT_DIR/modules/deepseek_hub/...` | CORRIGÉ — `wrappers/deepseek_student_cmd.sh` et `wrappers/deepseek_student_run_logged.sh` utilisent `$STUDENT_ROOT/scripts/deepseek_hub/`. |
| PATH fallback `modules/deepseek_thinking` / `modules/deepseek_response` dans `run_logged.sh` | NON TRAITÉ — dépendance externe légitime hors périmètre migration student. Déféré. |

## Exit Criteria

- all operator-facing docs use `/opt/trading/student`
- global shortcuts point to canonical facades
- no critical workflow depends on direct legacy paths
- duplicate wrappers are categorized as keep, merge, or retire
