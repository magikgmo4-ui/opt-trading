# 110_WHY_SCORE_MULTI_MACHINE_IMPACT

## Objectif

Integrer les impacts multi-machine dans le score WHY.

## Risques multi-machine

| Risque | Impact score |
| --- | --- |
| collision Git | penalite |
| divergence runtime | penalite critique |
| reprise incomplete | penalite importante |
| orchestration non documentee | penalite critique |
| machine cible ambigue | warning |

## Propagation critique

Les surfaces multi-machine:
- augmentent la criticite,
- augmentent le poids des invariants,
- augmentent le besoin de review humaine.

## Observation

Une surface simple sur une seule machine peut devenir critique lorsqu'elle participe a une chaine multi-machine.

## Invariant

Le score WHY ne doit jamais inferer une topologie machine sans preuve documentaire.

## RISKS

- À qualifier.
