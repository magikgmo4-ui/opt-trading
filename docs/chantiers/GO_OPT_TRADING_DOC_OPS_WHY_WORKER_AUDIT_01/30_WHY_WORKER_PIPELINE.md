# 30_WHY_WORKER_PIPELINE

## Objectif

Definir le pipeline du futur worker WHY.

## Pipeline candidat

1. DISCOVER
2. LOAD
3. PARSE
4. SCORE
5. DETECT_GAPS
6. ALIGN_RUNTIME
7. GENERATE_REPORTS
8. REVIEW_READY

## Etapes

| Etape | Role |
| --- | --- |
| DISCOVER | trouver documents cibles |
| LOAD | charger documents et sorties |
| PARSE | lire sections WHY |
| SCORE | calculer score WHY |
| DETECT_GAPS | detecter gaps critiques |
| ALIGN_RUNTIME | relier R0-R5 |
| GENERATE_REPORTS | produire sorties audit |
| REVIEW_READY | preparer review humaine |

## Etats speciaux

| Etat | Sens |
| --- | --- |
| SKIP | surface hors scope |
| ERROR | analyse impossible |
| PARTIAL | analyse incomplete |

## Invariant

Le pipeline ne doit jamais produire un APPLY runtime automatique.
