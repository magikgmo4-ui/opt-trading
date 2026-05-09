# 10_LINT_SCOPE

## Objectif

Definir le perimetre du WHY lint experimental.

## Scope

Le lint WHY est un controle documentaire experimental.

Il peut:
- lire les documents,
- detecter des sections manquantes,
- signaler des gaps,
- produire des warnings,
- preparer des rapports audit.

Il ne peut pas:
- modifier les fichiers,
- appliquer des corrections,
- bloquer une CI,
- valider un runtime,
- remplacer une review humaine.

## Surfaces candidates

| Surface | Lint |
| --- | --- |
| docs/chantiers | oui |
| docs/governance | oui |
| closeouts | oui |
| runtime reviews | oui |
| docs historiques | best effort |

## Hors scope

- auto-fix,
- CI bloquante,
- merge automatique,
- APPLY runtime,
- validation live.

## Invariant

Le lint WHY reste warning-only, lecture seule et non destructif.
