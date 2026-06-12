# CHECKPOINT

GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01

## État

| Livrable | Statut |
|----------|:------:|
| CAPABILITY_GATE_AND_FALLBACK_01.md | DRAFT |
| MODEL_TASK_BOUNDARY_MATRIX_01.md | DRAFT |
| RUNBOOK_MODEL_ESCALATION_01.md | DRAFT |

## Décisions figées

1. Le 0.5B est un probe de pipeline, pas un worker décisionnel
2. Tâche à format exact → escalader ou refuser
3. Tâche trading → REFUS
4. Pas de fallback distant disponible dans cette baseline

## Prochaine étape

Fermer le GO après merge. La chaîne complète est :
validation baseline → politique rétention → enforcement → smoke → adoption → usage contrôlé → gate capacité.

## RISKS

- À qualifier.
