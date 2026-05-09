# 20_RUNTIME_GRAPH_EDGE_TYPES

## Objectif

Definir les relations du futur WHY runtime graph system.

## Relations candidates

| Edge type | Sens |
| --- | --- |
| DEPENDS_ON | dependance technique ou governance |
| RUNS_ON | surface executee sur machine |
| GOVERNED_BY | relation governance |
| BLOCKED_BY | gate ou invariant bloquant |
| OBSERVED_BY | relation observabilite |
| RECOVERS_WITH | relation reprise |
| REVIEWED_BY | review humaine requise |
| CONNECTS_TO | liaison multi-surface |
| CLASSIFIED_AS | relation R0-R5 |
| REPORTS_TO | relation reporting |

## Regles

- Chaque relation doit etre explicable.
- Les dependances runtime critiques doivent etre visibles.
- Les relations multi-machine doivent etre documentees.
- Les relations externes doivent rester auditables.

## Observation

Le graphe doit aider a:
- visualiser les dependances,
- visualiser les risques,
- visualiser les gates,
- visualiser les surfaces critiques.

## Invariant

Aucune relation ne doit impliquer une orchestration runtime autonome.
