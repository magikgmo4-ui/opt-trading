# 20_BURN_DOWN_PLAN

## Priorités

| Priorité | WARN(s) | Sujet | Action | Dépendances |
|----------|---------|-------|--------|-------------|
| P0 | #2 | `.env` permissions | `chmod 600 .env` + audit | Aucune |
| P1 | #3, #4 | Registry drift AI-team | Corriger `tasks.index.json` | Aucune |
| P1 | #5, #6 | Sources handoff manquantes | Restaurer ou documenter suppression | Aucune |
| P1 | #9, #10, #11, #13 | Gmail/Calendar/Drive | Implémenter ou retirer du contrat actif | Décision HITL |
| P1 | #12 | KG repo index entries | Implémenter bricks ou retirer du registre | Aucune |
| P2 | #7 | FastAPI venv | Valider dépendance dans runtime cible | Aucune |
| P2 | #8 | Kill switch widget | Ajouter visibilité opérateur | Aucune |
| P3 | #1 | Strict worker E2E | Preuve modèle réelle read-only | Aucune |

## Ordre d'exécution

```
P0 ──► P1 (registry) ──► P1 (handoff) ──► P1 (gmail/calendar/drive) ──► P1 (KG index) ──► P2 ──► P3
```

Chaque groupe est indépendant et peut être parallélisé.

## Critères de succès

- Tous les WARN P0 et P1 : CLOSED ou CARRIED_FORWARD_WITH_REASON documenté
- Aucun nouveau WARN introduit
- Résumé final produit

## Gate finale

Le GO est clos quand :
1. Tous les WARN P0 sont CLOSED
2. Les WARN P1 sont CLOSED ou CARRIED_FORWARD_WITH_REASON
3. P2/P3 peuvent être CARRIED_FORWARD si justifié
4. Aucun secret exposé
5. `git diff --check` OK
