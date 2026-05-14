# 70_LOCAL_VIEW_OBSERVABILITY_ALIGNMENT

## Objectif

Relier le render WHY/runtime a l'observabilite runtime.

## Sources candidates

| Source | Usage |
| --- | --- |
| logs runtime | preuves execution |
| observability metadata | contexte runtime |
| snapshots | etat runtime |
| alerts | incidents critiques |
| review proofs | validation humaine |

## Alignements candidats

| Alignement | Usage |
| --- | --- |
| runtime proof overlay | preuves runtime |
| freshness overlay | validite snapshots |
| alert overlay | criticite runtime |
| governance proof overlay | validation humaine |

## Regles

- Les preuves runtime doivent rester visibles.
- Les overlays observabilite doivent rester explicables.
- Les validations humaines doivent rester auditables.
- Les surfaces critiques doivent rester contextualisees.

## Invariant

Le render WHY/runtime ne doit jamais inferer une preuve runtime absente.
