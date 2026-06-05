# 50_WHY_WORKER_EDGE_CASES

## Objectif

Identifier les cas limites du futur worker d'audit WHY.

## Cas limites

| ID | Cas limite | Politique |
| --- | --- | --- |
| WE-01 | parser retourne PARTIAL | continuer en mode degraded |
| WE-02 | score indisponible | produire rapport sans score |
| WE-03 | runtime class absente | marquer UNKNOWN |
| WE-04 | documents contradictoires | signaler IMPORTANT |
| WE-05 | document historique | mode informatif |
| WE-06 | surface R4/R5 incomplete | signaler CRITICAL |
| WE-07 | machine cible ambigue | signaler WARN |
| WE-08 | sortie parser malformee | ERROR local, batch continue |
| WE-09 | gap massif | rapport prioritaire |
| WE-10 | absence reprise | penalite importante |

## Regles

- Le worker doit continuer le batch si un document echoue.
- Les erreurs doivent etre localisees.
- Les resultats PARTIAL doivent etre explicites.
- Les surfaces R4/R5 doivent etre strictes.

## Invariant

Aucun cas limite ne doit declencher APPLY ou correction automatique.

## RISKS

- À qualifier.
