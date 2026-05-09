# 40_RUNTIME_GRAPH_MACHINE_RELATIONS

## Objectif

Integrer les relations multi-machine dans le WHY runtime graph.

## Machines connues

| Machine | Role |
| --- | --- |
| admin-trading | runtime trading |
| db-layer | orchestration et services |
| cursor-ai | observation et documentation |
| student | laboratoire IA |
| fantome | governance et continuite |

## Relations candidates

| Relation | Sens |
| --- | --- |
| RUNS_ON | runtime execute sur machine |
| DEPENDS_ON | dependance machine |
| OBSERVED_BY | observabilite distante |
| RECOVERS_WITH | reprise inter-machine |
| CONNECTS_TO | liaison reseau/logique |

## Risques critiques

| Risque | Impact |
| --- | --- |
| divergence machine | incoherence runtime |
| collision branches | derive governance |
| orchestration opaque | perte explicabilite |
| reprise incomplete | perte continuite |

## Regles

- Les dependances multi-machine doivent etre explicites.
- Les surfaces critiques doivent etre observables.
- Les reprises doivent etre documentees.
- Les chaines runtime critiques doivent etre reviewables humainement.

## Invariant

Le graphe ne doit jamais inferer une topologie machine non documentee.
