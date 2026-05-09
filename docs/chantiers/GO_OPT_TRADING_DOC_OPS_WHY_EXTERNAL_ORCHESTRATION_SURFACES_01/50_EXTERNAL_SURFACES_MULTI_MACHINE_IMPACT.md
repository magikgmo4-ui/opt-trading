# 50_EXTERNAL_SURFACES_MULTI_MACHINE_IMPACT

## Objectif

Integrer les impacts multi-machine des surfaces externes candidates.

## Impacts candidats

| Surface | Impact multi-machine |
| --- | --- |
| ClickUp | propagation statut cross-machine |
| Botpress | orchestration conversationnelle distribuee |
| Knowledge Graph | centralisation relationnelle |
| Airtable | coordination operations multi-surfaces |

## Risques critiques

| Risque | Impact |
| --- | --- |
| divergence machine | incoherence governance |
| sync partiel | etat runtime faux |
| orchestration opaque | perte explicabilite |
| collision statut | mauvaise priorisation |

## Regles

- Les dependances multi-machine doivent etre explicites.
- Les surfaces critiques doivent garder observabilite.
- Les reprises doivent etre documentees.
- Les collisions doivent etre detectables.

## Invariant

Aucune surface externe ne doit inferer seule une topologie multi-machine.
