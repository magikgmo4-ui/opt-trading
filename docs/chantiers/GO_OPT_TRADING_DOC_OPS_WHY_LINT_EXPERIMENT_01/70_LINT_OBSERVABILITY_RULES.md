# 70_LINT_OBSERVABILITY_RULES

## Objectif

Definir les regles observabilite du WHY lint experimental.

## Verifications candidates

| Verification | Usage |
| --- | --- |
| log source presente | preuves runtime |
| endpoint documente | observabilite |
| freshness exposee | reprise runtime |
| alertes exposees | detection risques |
| preuves review accessibles | governance |

## Detection candidate

| Cas | Warning |
| --- | --- |
| observabilite absente | HIGH |
| freshness inconnue | MEDIUM/HIGH |
| endpoint critique absent | HIGH |
| alertes absentes | MEDIUM |

## Regles

- Les surfaces critiques doivent rester observables.
- Les preuves runtime doivent etre tracables.
- Les surfaces multi-machine doivent exposer leurs preuves.
- Les surfaces externes doivent rester contextualisees.

## Invariant

Le lint WHY ne doit jamais inferer une observabilite runtime absente.

## RISKS

- À qualifier.
