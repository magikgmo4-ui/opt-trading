# 10_DASHBOARD_VIEW_TYPES

## Objectif

Definir les vues candidates du futur WHY governance dashboard.

## Vues candidates

| Vue | Role |
| --- | --- |
| WHY_OVERVIEW | synthese maturite WHY |
| RUNTIME_RISK | risques R0-R5 |
| GAP_MAP | gaps critiques |
| HUMAN_REVIEW | gates et reviews humaines |
| GRAPH_VIEW | runtime graph |
| EXTERNAL_SURFACES | ClickUp/Botpress/KG/Airtable |
| OBSERVABILITY | preuves runtime et freshness |
| WORKER_AUDIT | sorties worker WHY futures |
| LINT_EXPERIMENT | compatibilite lint futur |

## Regles

- Chaque vue doit rester explicable.
- Aucune vue ne doit declencher APPLY.
- Les vues critiques doivent exposer leurs limites.
- Les surfaces R4/R5 doivent garder review humaine.

## Invariant

Le dashboard doit visualiser et aider a auditer, jamais valider le runtime de maniere autonome.

## RISKS

- À qualifier.
