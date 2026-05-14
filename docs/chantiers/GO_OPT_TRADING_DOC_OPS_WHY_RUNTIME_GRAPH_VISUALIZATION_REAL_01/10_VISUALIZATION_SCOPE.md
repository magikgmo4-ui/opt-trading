# 10_VISUALIZATION_SCOPE

## Objectif

Definir le perimetre de la premiere visualisation reelle du WHY runtime graph.

## Scope initial

La visualisation couvre:
- composants WHY,
- surfaces runtime documentees,
- machines,
- classes R0-R5,
- gates humaines,
- observabilite,
- surfaces externes,
- relations governance/runtime.

## Hors scope initial

- dashboard live,
- graph traversal decisionnel,
- connecteurs live,
- APPLY runtime,
- CI active,
- modification automatique de documents.

## Vues candidates

| Vue | Role |
| --- | --- |
| graph global | vue generale WHY/runtime |
| machine view | surfaces par machine |
| R0-R5 overlay | criticite runtime |
| observability overlay | preuves runtime |
| review overlay | gates humaines |
| external surfaces overlay | ClickUp/Botpress/KG/Airtable |

## Invariant

La visualisation doit rester lecture seule et audit-oriented.
