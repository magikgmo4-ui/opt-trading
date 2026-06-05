# 50_WHY_SCORE_EDGE_CASES

## Objectif

Identifier les cas limites du futur WHY score generator.

## Cas limites

| ID | Cas limite | Politique |
| --- | --- | --- |
| SE-01 | document tres court mais valide | ne pas penaliser automatiquement |
| SE-02 | WHY implicite mais non titre | WARN, pas PASS |
| SE-03 | sections presentes mais vides | penaliser |
| SE-04 | sections contradictoires | penalite importante |
| SE-05 | R0 avec gaps nombreux | tolerer partiellement |
| SE-06 | R5 avec score moyen | signaler critique |
| SE-07 | document historique | score informatif seulement |
| SE-08 | closeout sans reprise | penaliser |
| SE-09 | runtime sans observabilite | penalite critique |
| SE-10 | gouvernance sans invariants | penalite critique |

## Regles

- Le score doit distinguer absence, presence vide et presence utile.
- Les documents historiques ne doivent pas bloquer la gouvernance courante.
- Les surfaces R4/R5 doivent rester strictes.

## Invariant

Les cas limites doivent etre expliques dans la sortie d'audit.

## RISKS

- À qualifier.
