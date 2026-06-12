# 40_LOCAL_VIEW_OUTPUTS

## Objectif

Definir les outputs reviewables du render graph reel local WHY/runtime.

## Outputs candidats

| Output | Usage |
| --- | --- |
| static graph image | visualisation locale |
| markdown snapshot | synthese governance |
| graph JSON export | integration future |
| overlay report | criticite runtime |
| review report | validation humaine |

## Caracteristiques attendues

| Caracteristique | Role |
| --- | --- |
| lecture seule | protection runtime |
| reviewable | validation humaine |
| exportable | integration future |
| contextualise | criticite runtime |
| multi-machine | orchestration distribuee |

## Outputs interdits

| Output | Raison |
| --- | --- |
| runtime control | interdit |
| orchestration runtime | interdit |
| auto-remediation | interdit |
| decision runtime | interdit |

## Invariant

Les outputs WHY/runtime doivent rester statiques, auditables et non destructifs.

## RISKS

- À qualifier.
