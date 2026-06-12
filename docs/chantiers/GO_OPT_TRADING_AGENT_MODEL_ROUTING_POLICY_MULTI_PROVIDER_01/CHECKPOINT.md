# CHECKPOINT

GO_OPT_TRADING_AGENT_MODEL_ROUTING_POLICY_MULTI_PROVIDER_01

## État

| Livrable | Statut |
|----------|:------:|
| MODEL_ROUTING_POLICY_MULTI_PROVIDER_01.md | DRAFT |
| TASK_TO_MODEL_CAPABILITY_MATRIX_01.md | DRAFT |
| RUNBOOK_PROVIDER_ESCALATION_01.md | DRAFT |

## Décisions figées

1. 0.5B agent chain = usage par défaut pour risque faible
2. Format exact → 1.5B direct Ollama ou REFUS
3. Raisonnement → deepseek-r1:1.5b direct Ollama
4. Aucun provider distant configuré → REFUS pour tâche critique
5. Pas de dégradation silencieuse

## Prochaine étape

Fermer le GO après merge.

## RISKS

- À qualifier.
