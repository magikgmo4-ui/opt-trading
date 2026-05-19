# 90_VISUALIZATION_STATIC_GRAPH_PROTOTYPE

## Objectif

Preparer le prototype graph statique reel du WHY runtime graph.

## Prototype cible

Le prototype doit produire une visualisation statique a partir de donnees documentaires existantes.

## Capacites candidates

| Capacite | Role |
| --- | --- |
| lire nodes documentes | construire le graphe |
| lire edges documentes | relier les surfaces |
| afficher machines | contexte multi-machine |
| afficher classes R0-R5 | criticite runtime |
| afficher gates humaines | review humaine |
| afficher observabilite | preuves runtime |

## Hors scope initial

- dashboard live,
- traversal decisionnel,
- connecteurs live,
- runtime temps reel,
- APPLY automatique,
- CI active.

## Regles

- Le prototype lit seulement.
- Le prototype rend seulement.
- Le prototype ne valide pas le runtime.
- Le prototype ne modifie pas les sources.

## Invariant

Le prototype statique doit rester audit-oriented et non destructif.
