# 70_RUNTIME_GRAPH_FAILURE_CHAINS

## Objectif

Formaliser les chaines de defaillance dans le WHY runtime graph.

## Chaines candidates

| Chaine | Exemple |
| --- | --- |
| machine -> runtime | panne machine -> service indisponible |
| runtime -> observabilite | endpoint down -> monitoring absent |
| governance -> orchestration | invariant absent -> derive runtime |
| external surface -> runtime | sync externe incoherent -> mauvaise priorisation |
| multi-machine -> reprise | divergence machines -> reprise incomplete |

## Relations critiques

| Relation | Risque |
| --- | --- |
| DEPENDS_ON | propagation panne |
| CONNECTS_TO | propagation incoherence |
| REPORTS_TO | derive statut |
| OBSERVED_BY | perte observabilite |

## Regles

- Les chaines critiques doivent etre visibles.
- Les surfaces R4/R5 doivent garder review humaine.
- Les chaines multi-machine doivent etre tracables.
- Les surfaces externes doivent rester contextualisees.

## Invariant

Le graphe doit aider a comprendre les chaines de risque sans automatiser les decisions runtime.

## RISKS

- À qualifier.
