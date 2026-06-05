# CHECKPOINT

GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01

## État actuel

| Élément | Statut |
|---------|:------:|
| Provider local CPU | PASS |
| Agent smoke canonique | PASS |
| Politique rétention documentée | DRAFT |
| Runbook rotation documenté | DRAFT |
| Automatisation cron | NON APPLIQUÉ |
| Session courante | vierge (66e1f924) |

## Prochaines étapes

1. [ ] Valider la politique en comité de revue
2. [ ] Tester rotation manuelle complète
3. [ ] Installer cron si validé
4. [ ] Fermer le GO

## Décisions en attente

- Faut-il automatiser la purge des archives > 30 jours ?
- Faut-il notifier sur saturation détectée ?
- Faut-il exposer un `/session rotate` pour l'agent ?

## Risques résiduels

- n_ctx=4096 limite structurelle du modèle sur ce CPU
- Pas de compaction automatique efficace dans OpenClaw actuel
- Rotation manuelle oubliable

## RISKS

- À qualifier.
