# 20_DASHBOARD_INPUT_MODEL

## Objectif

Definir les entrees du futur WHY governance dashboard.

## Entrees candidates

| Entree | Source |
| --- | --- |
| WHY parser outputs | parser WHY |
| WHY score outputs | score generator |
| worker audit reports | worker WHY |
| runtime graph reports | runtime graph |
| runtime classes R0-R5 | runtime governance |
| observability proofs | logs/endpoints/metrics |
| human review proofs | review runtime |
| external surfaces reports | ClickUp/Botpress/KG/Airtable |

## Types de donnees

| Type | Usage |
| --- | --- |
| markdown | syntheses humaines |
| json | sorties machine-readable |
| graph relations | visualisation runtime |
| review metadata | governance humaine |

## Regles

- Les entrees doivent etre tracables.
- Les preuves runtime doivent etre explicites.
- Les surfaces critiques doivent rester contextualisees.
- Les donnees externes doivent rester auditables.

## Invariant

Le dashboard ne doit jamais inferer des preuves runtime absentes.

## RISKS

- À qualifier.
