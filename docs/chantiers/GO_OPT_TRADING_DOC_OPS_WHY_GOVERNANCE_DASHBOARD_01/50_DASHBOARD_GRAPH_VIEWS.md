# 50_DASHBOARD_GRAPH_VIEWS

## Objectif

Definir les vues runtime graph du futur WHY governance dashboard.

## Vues candidates

| Vue | Role |
| --- | --- |
| GRAPH_OVERVIEW | vue globale du graphe |
| NODE_TYPES | types de noeuds |
| EDGE_TYPES | relations entre noeuds |
| FAILURE_CHAINS | chaines de defaillance |
| MACHINE_RELATIONS | relations multi-machine |
| EXTERNAL_RELATIONS | relations surfaces externes |
| REVIEW_GATES | gates humaines |

## Regles

- Chaque relation doit rester explicable.
- Les surfaces critiques doivent afficher leur classe R0-R5.
- Les gates humaines doivent etre visibles.
- Les surfaces externes doivent etre contextualisees.

## Invariant

La vue graph ne doit jamais devenir une orchestration runtime autonome.
