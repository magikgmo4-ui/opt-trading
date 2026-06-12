# 50_VISUALIZATION_MACHINE_OVERLAYS

## Objectif

Formaliser les overlays multi-machine du WHY runtime graph.

## Machines candidates

| Machine | Role |
| --- | --- |
| admin-trading | runtime critique |
| db-layer | orchestration et services |
| cursor-ai | governance documentaire |
| student | experimentation IA |
| fantome | supervision et continuite |

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| machine ownership | surfaces par machine |
| runtime dependencies | dependances cross-machine |
| recovery relations | chemins de reprise |
| observability relations | preuves runtime |
| governance relations | review humaine |

## Regles

- Les dependances critiques doivent etre visibles.
- Les surfaces R4/R5 doivent rester contextualisees.
- Les overlays multi-machine doivent rester explicables.
- Les chemins de reprise doivent rester auditables.

## Invariant

Les overlays multi-machine ne doivent jamais devenir une orchestration runtime autonome.

## RISKS

- À qualifier.
