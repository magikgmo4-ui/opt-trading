# 80_WHY_WORKER_MULTI_MACHINE_GOVERNANCE

## Objectif

Integrer la governance multi-machine dans le futur worker WHY.

## Machines connues

| Machine | Role |
| --- | --- |
| admin-trading | runtime trading |
| db-layer | orchestration |
| cursor-ai | docs et observation |
| student | laboratoire IA |
| fantome | governance |

## Regles candidates

- Les surfaces multi-machine doivent etre considerees plus critiques.
- Les dependances runtime doivent etre explicites.
- Les reprises doivent etre documentees.
- Les collisions Git doivent etre penalisees.

## Risques multi-machine

| Risque | Impact |
| --- | --- |
| divergence runtime | critique |
| collision branches | important |
| reprise incomplete | important |
| observabilite absente | critique |
| orchestration opaque | critique |

## Invariant

Le worker WHY ne doit jamais inferer une topologie multi-machine sans preuve documentaire explicite.

## RISKS

- À qualifier.
