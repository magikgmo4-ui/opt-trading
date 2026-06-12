# 50_LOCAL_VIEW_OVERLAYS

## Objectif

Formaliser les overlays WHY/runtime du render graph reel local.

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| R0-R5 severity | criticite runtime |
| governance gates | validation humaine |
| observability status | preuves runtime |
| machine ownership | contexte multi-machine |
| recovery paths | reprise runtime |
| warning layer | gaps WHY/lint |

## Regles

- Les overlays doivent rester explicables.
- Les surfaces critiques doivent rester contextualisees.
- Les warnings ne doivent pas devenir bloquants.
- Les overlays ne doivent pas modifier les sources.

## Limites

- Pas d'overlays live.
- Pas de runtime temps reel.
- Pas de correction automatique.
- Pas de decision runtime.

## Invariant

Les overlays WHY/runtime doivent rester statiques, reviewables et non destructifs.

## RISKS

- À qualifier.
