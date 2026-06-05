# 70_VISUALIZATION_OBSERVABILITY_OVERLAYS

## Objectif

Formaliser les overlays observabilite du WHY runtime graph.

## Sources candidates

| Source | Usage |
| --- | --- |
| logs runtime | preuves execution |
| endpoints | verification services |
| snapshots | etat runtime |
| metrics | criticite runtime |
| alerts | detection incidents |
| review proofs | validation humaine |

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| observability status | preuves runtime |
| freshness status | validite snapshots |
| alert overlays | incidents critiques |
| runtime proof overlays | verification runtime |
| review proof overlays | validation humaine |

## Regles

- Les preuves runtime doivent rester visibles.
- Les surfaces critiques doivent rester observables.
- Les overlays observabilite doivent rester explicables.
- Les preuves review humaine doivent rester accessibles.

## Invariant

Les overlays observabilite ne doivent jamais inferer des preuves runtime absentes.

## RISKS

- À qualifier.
