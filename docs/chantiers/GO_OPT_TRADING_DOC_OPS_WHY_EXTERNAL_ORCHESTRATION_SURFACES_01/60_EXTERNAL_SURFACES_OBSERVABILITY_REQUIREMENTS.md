# 60_EXTERNAL_SURFACES_OBSERVABILITY_REQUIREMENTS

## Objectif

Definir l'observabilite minimale des surfaces externes candidates.

## Exigences candidates

| Exigence | Role |
| --- | --- |
| journaux explicites | auditabilite |
| source identifiable | tracabilite |
| timestamp fiable | reprise |
| machine source connue | contexte runtime |
| provenance donnees | coherence governance |

## Observation

Les surfaces externes deviennent dangereuses si:
- les donnees ne sont pas tracables,
- les mises a jour sont opaques,
- les propagations ne sont pas visibles.

## Regles

- Toute propagation doit etre explicable.
- Toute source doit etre identifiable.
- Toute synchronisation critique doit etre observable.
- Toute decision critique doit rester reviewable humainement.

## Invariant

Aucune surface externe ne doit devenir une boite noire runtime.

## RISKS

- À qualifier.
