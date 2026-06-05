# 10_STATIC_PROTOTYPE_SCOPE

## Objectif

Definir le perimetre du premier prototype graph statique WHY/runtime.

## Scope initial

Le prototype doit produire un rendu statique local a partir de sources documentaires autorisees.

Il couvre:
- nodes WHY,
- nodes runtime,
- machines,
- relations documentees,
- classes R0-R5,
- overlays observabilite,
- overlays review humaine.

## Hors scope initial

- runtime live,
- connecteurs live,
- dashboard live,
- traversal decisionnel,
- APPLY runtime,
- CI active,
- auto-correction documentaire.

## Capacites candidates

| Capacite | Role |
| --- | --- |
| lire docs | extraire relations documentees |
| lire JSON statique | importer graph candidates |
| rendre graph | produire vue statique |
| exporter artefacts | produire fichiers reviewables |

## Invariant

Le prototype statique WHY/runtime doit rester lecture seule, local et audit-oriented.

## RISKS

- À qualifier.
