# 50_RUNTIME_GRAPH_EXTERNAL_SURFACES

## Objectif

Integrer les surfaces externes candidates dans le futur WHY runtime graph.

## Surfaces externes candidates

| Surface | Node type | Classe candidate | Role |
| --- | --- | --- | --- |
| ClickUp | EXTERNAL_SURFACE | R2/R3 | suivi / priorisation |
| Botpress | EXTERNAL_SURFACE | R3 | orchestration conversationnelle |
| Knowledge Graph | EXTERNAL_SURFACE | R3 | coherence relationnelle |
| Airtable | EXTERNAL_SURFACE | R2/R3 | structuration operations |

## Relations candidates

| Surface | Relations |
| --- | --- |
| ClickUp | REPORTS_TO, GOVERNED_BY, CONNECTS_TO |
| Botpress | CONNECTS_TO, GOVERNED_BY, REVIEWED_BY |
| Knowledge Graph | DEPENDS_ON, GOVERNED_BY, REPORTS_TO |
| Airtable | REPORTS_TO, CONNECTS_TO, GOVERNED_BY |

## Regles

- Les surfaces externes restent candidates tant qu'aucune integration active n'est validee.
- Les relations externes doivent rester auditables.
- Les surfaces externes ne doivent pas etre promues R4/R5 sans governance explicite.
- Toute relation externe critique doit garder review humaine.

## Invariant

Le graphe ne doit jamais transformer une surface externe en orchestrateur runtime autonome.
