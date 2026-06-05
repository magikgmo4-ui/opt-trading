# 30_RUNTIME_GRAPH_RUNTIME_CLASSES

## Objectif

Integrer les classes runtime R0-R5 dans le futur WHY runtime graph.

## Mapping candidat

| Classe | Sens dans le graphe |
| --- | --- |
| R0 | information/documentation |
| R1 | faible criticite |
| R2 | orchestration moderee |
| R3 | orchestration critique contextualisee |
| R4 | runtime critique |
| R5 | runtime critique maximal |

## Regles

- Les noeuds critiques doivent exposer leur classe runtime.
- Les surfaces multi-machine augmentent la criticite potentielle.
- Les surfaces externes ne doivent pas etre promues R4/R5 sans governance explicite.
- Les relations R4/R5 doivent garder review humaine.

## Observation

Le graphe doit permettre de:
- visualiser les zones critiques,
- identifier les chaines de risque,
- comprendre les dependances runtime.

## Invariant

La classe runtime doit rester contextualisee et explicable.

## RISKS

- À qualifier.
