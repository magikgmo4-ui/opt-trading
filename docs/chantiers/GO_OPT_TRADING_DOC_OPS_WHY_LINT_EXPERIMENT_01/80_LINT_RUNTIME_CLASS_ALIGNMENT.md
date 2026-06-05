# 80_LINT_RUNTIME_CLASS_ALIGNMENT

## Objectif

Definir les alignements R0-R5 du WHY lint experimental.

## Alignements candidats

| Classe | Verification candidate |
| --- | --- |
| R0 | structure documentaire minimale |
| R1 | WHY present |
| R2 | observabilite recommandee |
| R3 | review humaine recommandee |
| R4 | review humaine obligatoire |
| R5 | review humaine + observabilite + recovery path obligatoires |

## Detection candidate

| Cas | Warning |
| --- | --- |
| classe absente | MEDIUM |
| R4 sans review | CRITICAL |
| R5 sans observabilite | CRITICAL |
| R5 sans recovery path | CRITICAL |
| runtime critique sans WHY | CRITICAL |

## Regles

- Les surfaces critiques doivent augmenter la severite.
- Les surfaces multi-machine doivent etre contextualisees.
- Les surfaces externes doivent rester auditables.
- Les incoherences runtime/governance doivent etre visibles.

## Invariant

Le lint WHY ne doit jamais promouvoir automatiquement une classe runtime.

## RISKS

- À qualifier.
