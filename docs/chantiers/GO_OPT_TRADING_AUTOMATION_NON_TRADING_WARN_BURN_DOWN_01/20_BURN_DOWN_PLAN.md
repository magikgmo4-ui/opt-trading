# 20_BURN_DOWN_PLAN

## Priorités — Résolues

| Priorité | WARN(s) | Sujet | Action | Statut final |
|----------|---------|-------|--------|-------------|
| P0 | #2 | `.env` permissions | `chmod 600 .env` + audit | **CLOSED** |
| P1 | #3, #4 | Registry drift AI-team | Corriger `tasks.index.json` | **CLOSED** |
| P1 | #5, #6 | Sources handoff manquantes | Déclassifié (obsolètes) | **DECLASSIFIED** |
| P1 | #9, #10 | Gmail / Calendar | Retirés du périmètre actif | **DECLASSIFIED** |
| P1 | #11, #13 | Drive bridge + canary | Canary packet créé, Drive actif | **CLOSED** |
| P1 | #12 | KG repo index entries | Ratio index/bricks 1:1 vérifié | **DECLASSIFIED** |
| P2 | #7 | FastAPI venv | Faux positif (présent dans venv + requirements) | **DECLASSIFIED** |
| P2 | #8 | Kill switch widget | Présent dans Automation Cockpit | **DECLASSIFIED** |
| P3 | #1 | Strict worker E2E | E2E test exécuté, verdict PASS | **CLOSED** |

## Ordre d'exécution

```
P0 ──► P1 (registry) ──► P1 (handoff) ──► P1 (gmail/calendar/drive) ──► P1 (KG index) ──► P2 ──► P3
```

Chaque groupe est indépendant et peut être parallélisé.

## Critères de succès — Atteints

- [x] Tous les WARN P0 et P1 : CLOSED ou DECLASSIFIED
- [x] Aucun CARRIED_FORWARD restant
- [x] Aucun nouveau WARN introduit
- [x] Résumé final produit

## Gate finale — PASS

Le GO est clos car :
1. [x] Tous les WARN P0 sont CLOSED
2. [x] Tous les WARN P1 sont CLOSED ou DECLASSIFIED
3. [x] P2/P3 sont CLOSED ou DECLASSIFIED
4. [x] Aucun secret exposé
5. [x] `git diff --check` OK
6. [x] **13/13 WARN résolus — 0 CARRIED_FORWARD, 0 BLOCKER**
