# 110_WHY_PARSER_MULTI_MACHINE_CONTEXT

## Objectif

Integrer le contexte multi-machine dans le futur parser WHY.

## Machines connues

| Machine | Role |
| --- | --- |
| admin-trading | runtime trading |
| db-layer | orchestration |
| cursor-ai | docs et observation |
| student | laboratoire IA |
| fantome | gouvernance |

## Regles candidates

- Le parser doit detecter les references machine.
- Les surfaces multi-machine doivent etre marquees plus critiques.
- Les documents mentionnant orchestration doivent etre rapproches des classes R3+.
- Les references runtime live doivent etre rapprochees des classes R4/R5.

## Risques multi-machine

| Risque | Impact |
| --- | --- |
| collision Git | etat incoherent |
| divergence runtime | mauvaises decisions |
| reprise incomplete | interruption operatoire |
| hallucination documentaire | mauvaise classification |

## Invariant

Le parser ne doit jamais inferer une machine cible sans preuve documentaire explicite.
