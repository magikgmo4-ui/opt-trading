# 20_WHY_SCORE_WEIGHTING

## Objectif

Definir les ponderations candidates du score WHY.

## Pondérations candidates

| Composante | R0/R1 | R2/R3 | R4/R5 |
| --- | --- | --- | --- |
| WHY | 10 | 10 | 15 |
| INVARIANTS | 5 | 15 | 20 |
| FAILURE_MODES | 5 | 15 | 20 |
| GATES | 5 | 15 | 20 |
| RESUME_POINT | 10 | 10 | 10 |
| CANONICAL_STATE | 10 | 10 | 10 |
| OBSERVABILITY | 0 | 10 | 15 |
| HUMAN_REVIEW | 0 | 5 | 20 |

## Observation

Les surfaces critiques doivent:
- augmenter le poids des invariants,
- augmenter le poids des gates,
- augmenter le poids de la review humaine.

## Invariant

Les ponderations doivent rester explicables et auditables.
