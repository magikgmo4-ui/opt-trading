# 60_STATIC_PROTOTYPE_MULTI_MACHINE_MODEL

## Objectif

Formaliser le modele multi-machine du prototype WHY/runtime.

## Machines candidates

| Machine | Role |
| --- | --- |
| admin-trading | runtime critique |
| db-layer | orchestration |
| cursor-ai | governance documentaire |
| student | experimentation IA |
| fantome | supervision |

## Relations candidates

| Relation | Usage |
| --- | --- |
| RUNS_ON | execution runtime |
| OBSERVED_BY | observabilite distante |
| RECOVERS_WITH | reprise inter-machine |
| REVIEWED_BY | governance humaine |
| DEPENDS_ON | dependances runtime |

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| machine ownership | surfaces runtime |
| critical propagation | propagation risques |
| observability context | preuves runtime |
| governance context | review humaine |

## Invariant

Le modele multi-machine WHY/runtime ne doit jamais devenir une orchestration distribuee autonome.
