# 70_EXTERNAL_SURFACES_RUNTIME_BOUNDARIES

## Objectif

Verrouiller les frontieres runtime des surfaces externes.

## Frontieres candidates

| Surface | Limite runtime |
| --- | --- |
| ClickUp | suivi seulement |
| Botpress | assistance seulement |
| Knowledge Graph | relationnel seulement |
| Airtable | structuration seulement |

## Interdictions candidates

| Interdiction | Raison |
| --- | --- |
| APPLY automatique | protection runtime |
| merge automatique | governance humaine |
| execution live autonome | criticite runtime |
| propagation runtime implicite | derive orchestration |

## Regles

- Les surfaces externes doivent rester contextualisees.
- Les integrations runtime doivent etre explicites.
- Les surfaces critiques doivent garder review humaine.
- Les limites doivent etre documentees.

## Invariant

Aucune surface externe ne doit devenir un orchestrateur runtime autonome sans governance explicite.
