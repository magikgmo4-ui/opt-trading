# 20_WORKFLOW_RESULTS — Résultats après correction

Les corrections sont appliquées dans ce commit. Un nouveau déclenchement est nécessaire pour confirmer le PASS.

| Workflow | Run initial | Cause échec | Correction | Statut attendu |
|----------|-------------|-------------|------------|----------------|
| Validate | FAIL | `TASKS_INDEX_PATH` manquant | Ajout env vars | PASS (après prochain run) |
| Smoke | FAIL | `--job-packet` flag invalide | Arg positionnel | PASS (après prochain run) |
| Schedule | non déclenché (cron) | N/A | N/A | PASS (cron lun 8h UTC) |

## Schedule

Le workflow `strict-workers-schedule.yml` est configuré avec cron `0 8 * * 1` (lundi 8h UTC). Il n'a pas été déclenché manuellement car identique au smoke après la correction.
