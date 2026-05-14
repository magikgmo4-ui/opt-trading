# 60_VISUALIZATION_R0_R5_OVERLAYS

## Objectif

Formaliser les overlays criticite R0-R5 du WHY runtime graph.

## Classes runtime

| Classe | Sens |
| --- | --- |
| R0 | informationnel |
| R1 | faible criticite |
| R2 | orchestration moderee |
| R3 | runtime contextualise |
| R4 | runtime critique |
| R5 | criticite maximale |

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| runtime severity | criticite surfaces |
| governance gates | review humaine requise |
| observability requirements | preuves runtime |
| recovery requirements | chemins reprise |
| dependency propagation | propagation risques |

## Regles

- Les surfaces critiques doivent rester visibles.
- Les surfaces R4/R5 doivent garder review humaine.
- Les overlays criticite doivent rester contextualises.
- Les propagations critiques doivent rester auditables.

## Invariant

Les overlays R0-R5 ne doivent jamais devenir une validation runtime autonome.
