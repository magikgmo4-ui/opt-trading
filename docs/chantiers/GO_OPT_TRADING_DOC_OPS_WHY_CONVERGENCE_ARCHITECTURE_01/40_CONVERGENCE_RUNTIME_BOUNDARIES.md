# 40_CONVERGENCE_RUNTIME_BOUNDARIES

## Objectif

Verrouiller les frontieres runtime/governance de la convergence WHY.

## Frontieres principales

| Frontiere | Protection |
| --- | --- |
| aucun APPLY automatique | protection runtime |
| aucun merge automatique | governance humaine |
| aucun worker runtime autonome | criticite runtime |
| aucun dashboard live autonome | review humaine |
| aucun lint bloquant | experimentation seulement |

## Regles

- Les composants WHY doivent rester audit-oriented.
- Les surfaces critiques doivent garder review humaine.
- Les surfaces R4/R5 doivent garder observabilite et recovery paths.
- Les integrations futures doivent rester progressives.

## Surfaces futures candidates

| Surface | Etat |
| --- | --- |
| worker WHY reel | futur |
| graph traversal runtime | futur |
| dashboard live | futur |
| lint governance non bloquant | futur |
| CI governance experimentale | futur |
| visualisation multi-machine | futur |
| scoring dynamique WHY/runtime | futur |

## Invariant

La convergence WHY ne doit jamais devenir une orchestration runtime autonome sans governance explicite.

## RISKS

- À qualifier.
