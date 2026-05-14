# 10_STATIC_VIEW_SCOPE

## Objectif

Definir le perimetre de la vue statique locale WHY/runtime.

## Scope initial

La vue statique doit couvrir:
- composants WHY,
- surfaces runtime documentees,
- machines,
- relations governance/runtime,
- classes R0-R5,
- gates humaines,
- overlays observabilite.

## Hors scope initial

- runtime live,
- connecteurs live,
- traversal decisionnel,
- dashboard live,
- CI active,
- APPLY runtime.

## Vues candidates

| Vue | Role |
| --- | --- |
| global static graph | vue WHY/runtime globale |
| machine static graph | vue par machine |
| R0-R5 overlay | criticite runtime |
| review overlay | gates humaines |
| observability overlay | preuves runtime |

## Invariant

La vue statique WHY/runtime doit rester lecture seule, locale et non destructive.
