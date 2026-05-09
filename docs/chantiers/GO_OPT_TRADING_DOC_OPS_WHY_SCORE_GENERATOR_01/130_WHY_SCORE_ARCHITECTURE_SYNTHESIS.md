# 130_WHY_SCORE_ARCHITECTURE_SYNTHESIS

## Objectif

Synthétiser l'architecture du WHY score generator.

## Synthese

Le chantier definit un score WHY:
- explicable,
- contextualise,
- audit-oriented,
- non destructif,
- relie a R0-R5,
- prepare pour integration worker WHY.

## Architecture retenue

| Couche | Role |
| --- | --- |
| score model | definir composantes |
| weighting | contextualiser criticite |
| penalties | penaliser gaps critiques |
| runtime relation | aligner R0-R5 |
| edge cases | gerer cas limites |
| false confidence policy | limiter derive confiance |
| explainability | rendre score lisible |
| audit outputs | produire sorties audit |
| state machine | definir pipeline score |
| runtime alignment | relier governance runtime |
| multi-machine impact | integrer dependances |
| worker integration | preparer audit futur |

## Invariant final

Le score WHY ne doit jamais remplacer:
- review humaine,
- preuve runtime,
- governance critique.
