# 120_WHY_WORKER_ROADMAP

## Objectif

Preparer la roadmap du futur worker WHY.

## Phases candidates

| Phase | Objectif |
| --- | --- |
| V1 | parser markdown WHY |
| V2 | detection de gaps |
| V3 | scoring WHY |
| V4 | audit multi-machine |
| V5 | lint documentaire experimental |
| V6 | dashboard governance |

## Dependances

| Composant | Necessaire avant |
| --- | --- |
| parser stable | scoring |
| scoring stable | worker audit |
| governance WHY stable | lint experimental |
| runtime map stable | audit multi-machine |
| donnees stables | dashboard |

## Invariants

- Aucun APPLY automatique.
- Aucun merge automatique.
- Aucune autorite runtime autonome.
- Worker audit uniquement.

## Direction future

Le worker pourrait plus tard:
- produire des rapports WHY,
- produire des cartes runtime,
- detecter les gaps critiques,
- assister les reviews humaines.

## Resume point

Avant implementation:
- stabiliser conventions markdown,
- stabiliser scoring,
- stabiliser classes runtime,
- stabiliser governance WHY.
