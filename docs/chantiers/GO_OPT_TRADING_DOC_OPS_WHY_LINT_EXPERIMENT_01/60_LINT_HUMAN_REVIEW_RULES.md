# 60_LINT_HUMAN_REVIEW_RULES

## Objectif

Definir les regles review humaine du WHY lint experimental.

## Regles candidates

| Verification | Importance |
| --- | --- |
| review humaine presente | critique |
| gate review documentee | importante |
| preuves runtime accessibles | importante |
| validation contextualisee | importante |

## Surfaces critiques

Les surfaces:
- R4,
- R5,
- multi-machine,
- runtime critique,

doisvent exiger une review humaine explicite.

## Detection candidate

| Cas | Warning |
| --- | --- |
| review absente | HIGH/CRITICAL |
| gate review absente | HIGH |
| preuve runtime absente | HIGH |
| validation implicite | CRITICAL |

## Invariant

Le lint WHY ne doit jamais remplacer une review humaine critique.

## RISKS

- À qualifier.
