# 120_LINT_WORKER_INTEGRATION_ROADMAP

## Objectif

Preparer l'integration future du WHY lint experimental avec le worker WHY reel.

## Phases candidates

| Phase | Objectif |
| --- | --- |
| V1 | detection gaps documentaire |
| V2 | alignement runtime/governance |
| V3 | integration observabilite |
| V4 | integration runtime graph |
| V5 | integration governance dashboard |
| V6 | integration worker WHY |
| V7 | experimentation CI governance |

## Dependances

| Composant | Necessaire avant |
| --- | --- |
| parser WHY | lint structure |
| score generator | lint severity |
| runtime graph | coherence runtime |
| dashboard WHY | visualisation |
| worker WHY stable | integration lint |

## Regles

- L'integration doit rester progressive.
- Les surfaces critiques doivent garder review humaine.
- Les warnings doivent rester contextualises.
- Les limites runtime doivent rester explicites.

## Invariant

Le lint WHY ne doit jamais devenir un worker runtime autonome.
