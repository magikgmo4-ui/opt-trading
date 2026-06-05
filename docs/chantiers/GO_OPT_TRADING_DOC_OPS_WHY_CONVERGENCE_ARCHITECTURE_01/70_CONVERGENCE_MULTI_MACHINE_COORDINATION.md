# 70_CONVERGENCE_MULTI_MACHINE_COORDINATION

## Objectif

Formaliser la coordination multi-machine de la convergence WHY.

## Machines candidates

| Machine | Role |
| --- | --- |
| admin-trading | runtime critique |
| db-layer | orchestration et services |
| cursor-ai | governance et documentation |
| student | experimentation IA |
| fantome | continuite et supervision |

## Relations candidates

| Relation | Usage |
| --- | --- |
| RUNS_ON | execution runtime |
| OBSERVED_BY | observabilite distante |
| RECOVERS_WITH | reprise inter-machine |
| CONNECTS_TO | dependances runtime |
| REVIEWED_BY | governance humaine |

## Regles

- Les surfaces multi-machine doivent rester contextualisees.
- Les dependances critiques doivent etre visibles.
- Les reprises doivent etre documentees.
- Les surfaces R4/R5 doivent garder review humaine.

## Invariant

La convergence WHY ne doit jamais inferer une orchestration multi-machine non documentee.

## RISKS

- À qualifier.
