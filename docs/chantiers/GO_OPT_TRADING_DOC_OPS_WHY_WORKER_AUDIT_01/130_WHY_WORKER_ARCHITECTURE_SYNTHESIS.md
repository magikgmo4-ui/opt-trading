# 130_WHY_WORKER_ARCHITECTURE_SYNTHESIS

## Objectif

Synthétiser l'architecture du futur worker d'audit WHY.

## Synthese

Le chantier definit un worker WHY:
- audit-oriented,
- non destructif,
- multi-machine aware,
- relie au parser WHY,
- relie au score generator,
- relie a la governance runtime,
- prepare pour reporting humain et machine-readable.

## Architecture retenue

| Couche | Role |
| --- | --- |
| worker scope | definir les limites du worker |
| worker inputs | definir les sources parser/scoring/runtime |
| worker pipeline | formaliser le flux audit |
| worker outputs | produire rapports audit |
| edge cases | gerer analyse partielle et erreurs locales |
| runtime limits | proteger surfaces critiques |
| human review policy | preserver decision humaine |
| multi-machine governance | integrer dependances machines |
| state machine | definir transitions worker |
| runtime alignment | relier worker a R0-R5 |
| reporting architecture | structurer les rapports |
| autonomy limits | bloquer autonomie critique |

## Pipeline cible

1. DISCOVER
2. LOAD
3. PARSE_ATTACH
4. SCORE_ATTACH
5. GAP_ANALYZE
6. RUNTIME_ALIGN
7. MULTI_MACHINE_CHECK
8. REVIEW_CLASSIFY
9. REPORT_BUILD
10. REVIEW_READY

## Pourquoi cette architecture existe

Le WHY worker doit aider a auditer les documents sans devenir un agent autonome de validation runtime.

Il doit rendre visibles:
- les gaps,
- les scores,
- les risques,
- les surfaces critiques,
- les besoins de review humaine.

## Invariant final

Le worker WHY ne doit jamais modifier les documents, merger une branche, declencher APPLY ou remplacer une review humaine sur surface critique.

## RISKS

- À qualifier.
