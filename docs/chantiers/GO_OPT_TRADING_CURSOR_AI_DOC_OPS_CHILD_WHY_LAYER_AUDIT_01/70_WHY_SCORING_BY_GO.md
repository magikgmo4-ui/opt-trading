# 70_WHY_SCORING_BY_GO

## Objectif

Evaluer la maturite WHY d'un GO.

## Grille

| Critere | Score |
| --- | --- |
| WHY explicite | /5 |
| Invariants documentes | /5 |
| Failure modes identifies | /5 |
| Tradeoffs documentes | /5 |
| Separation audit/apply | /5 |
| Reprise claire | /5 |
| Etat reel prouve | /5 |
| Protection runtime | /5 |
| Intention produit explicite | /5 |
| Anti-derive IA | /5 |

## Niveaux

| Score | Niveau |
| --- | --- |
| 0-20 | Procedural only |
| 21-35 | WHY faible |
| 36-45 | WHY solide |
| 46-50 | IA-oriented governance |

## Observation

Le repo opt-trading contient deja plusieurs GO entre 36 et 45.

Les meilleurs candidats WHY:
- gouvernance,
- DB layer gating,
- collectors doctrine,
- machine split,
- reprise parents.

## RISKS

- À qualifier.
