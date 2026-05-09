# 10_WHY_WORKER_SCOPE

## Objectif

Definir le role du futur worker d'audit WHY.

## Role

Le worker WHY est un composant d'audit documentaire.

Il peut:
- scanner les documents,
- lire les sorties parser,
- lire les scores WHY,
- detecter les gaps,
- produire des rapports.

Il ne peut pas:
- modifier le runtime,
- modifier les documents,
- merger une branche,
- bloquer une execution live,
- remplacer une review humaine.

## Surfaces cibles

| Surface | Role |
| --- | --- |
| docs/governance | doctrine WHY |
| docs/chantiers | GO et closeouts |
| docs/index | routage et references |
| runtime reviews | surfaces critiques |

## Non-objectifs

- pas de CI active,
- pas d'enforcement bloquant,
- pas de correction automatique,
- pas d'APPLY.

## Invariant

Le worker WHY reste audit-oriented et non destructif.
