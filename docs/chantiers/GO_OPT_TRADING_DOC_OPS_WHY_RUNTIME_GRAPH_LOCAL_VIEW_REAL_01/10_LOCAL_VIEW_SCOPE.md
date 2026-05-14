# 10_LOCAL_VIEW_SCOPE

## Objectif

Definir le perimetre du premier render graph reel local WHY/runtime.

## Scope initial

Le local view real doit couvrir:
- composants WHY,
- surfaces runtime documentees,
- machines,
- relations governance/runtime,
- classes R0-R5,
- overlays observabilite,
- overlays review humaine.

## Hors scope initial

- runtime live,
- connecteurs live,
- traversal decisionnel,
- dashboard live,
- CI active,
- APPLY runtime,
- modification automatique des sources.

## Capacites candidates

| Capacite | Role |
| --- | --- |
| charger sources statiques | preparer le graph |
| construire nodes/edges | produire structure locale |
| appliquer overlays | contextualiser WHY/runtime |
| produire artefacts | rendre reviewable |

## Invariant

Le render local WHY/runtime doit rester lecture seule, local et non destructif.
