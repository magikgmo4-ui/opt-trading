# CHECKPOINT

GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01

## État

| Segment | Statut |
|---------|:------:|
| Baseline runtime | ADOPTED |
| Runbook usage contrôlé | DRAFT |
| Intégration continue | NON APPLIQUÉ |

## Règles d'usage contrôlé

1. Toujours vérifier gateway + session avant lancement
2. Ne jamais utiliser pour du trading sans GO dédié
3. Rotation obligatoire après 10 runs
4. Diagnostic systématique avant retry
5. Prewarm recommandé
6. Smoke de vérification après rotation

## Prochaine étape

Fermer le GO après merge. La baseline Student/Ollama est maintenant complète :
validation → politique → enforcement → baseline adoption → usage runbook.

## RISKS

- À qualifier.
