# 60_RUNTIME_GRAPH_OBSERVABILITY_NODES

## Objectif

Integrer les preuves runtime et l'observabilite dans le WHY runtime graph.

## Noeuds observabilite candidats

| Node | Role |
| --- | --- |
| LOG_SOURCE | journaux et traces |
| ENDPOINT | endpoint runtime |
| HEALTH_CHECK | verification runtime |
| SNAPSHOT | etat capture |
| METRIC | mesure runtime |
| ALERT | signal critique |
| REVIEW_PROOF | preuve review humaine |

## Relations candidates

| Relation | Sens |
| --- | --- |
| OBSERVED_BY | surface observee |
| REPORTS_TO | reporting runtime |
| VALIDATED_BY | preuve runtime |
| REVIEWED_BY | review humaine associee |

## Regles

- Les surfaces critiques doivent etre observables.
- Les preuves runtime doivent etre tracables.
- Les reviews humaines doivent etre representables.
- Les chaines critiques doivent rester explicables.

## Invariant

Le graphe ne doit jamais inferer une preuve runtime absente.
