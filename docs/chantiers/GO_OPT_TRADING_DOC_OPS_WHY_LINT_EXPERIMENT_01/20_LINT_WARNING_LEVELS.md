# 20_LINT_WARNING_LEVELS

## Objectif

Definir les niveaux warning-only du WHY lint experimental.

## Niveaux candidats

| Niveau | Sens |
| --- | --- |
| INFO | information contextuelle |
| LOW | faible risque documentaire |
| MEDIUM | gap important |
| HIGH | risque governance/runtime |
| CRITICAL | surface critique incomplete |

## Regles

- Aucun niveau ne bloque automatiquement.
- Les surfaces R4/R5 doivent augmenter la severite potentielle.
- Les warnings doivent rester explicables.
- Les warnings doivent rester auditables.

## Exemples

| Cas | Niveau |
| --- | --- |
| section WHY manquante | LOW/MEDIUM |
| recovery path absent | HIGH |
| review humaine absente sur R5 | CRITICAL |
| observabilite absente | HIGH |

## Invariant

Le lint WHY ne doit jamais transformer un warning en action runtime autonome.
