# 30_EXTERNAL_SURFACES_AUTONOMY_RISK

## Objectif

Evaluer les risques d'autonomie IA des surfaces externes.

## Risques candidats

| Surface | Risque autonomie |
| --- | --- |
| ClickUp | propagation automatique de statut |
| Botpress | action conversationnelle autonome |
| Knowledge Graph | inference abusive |
| Airtable | derive orchestration data-driven |

## Risques critiques

| Risque | Impact |
| --- | --- |
| boucle automation | derive runtime |
| hallucination structurelle | mauvaises decisions |
| orchestration opaque | perte explicabilite |
| score sans review | fausse confiance |

## Regles

- Toute autonomie doit rester explicable.
- Les surfaces critiques doivent garder review humaine.
- Les integrations doivent rester audit-oriented.
- Les boucles automation doivent etre interdites sans governance forte.

## Invariant

Aucune surface externe ne doit obtenir d'autonomie runtime implicite.
