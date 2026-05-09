# 30_LINT_DOCUMENT_TARGETS

## Objectif

Definir les surfaces documentaires ciblees par le WHY lint experimental.

## Documents candidats

| Surface | Priorite |
| --- | --- |
| 00_INITIAL_PROJECT_DOC | critique |
| closeouts | critique |
| runtime governance docs | critique |
| runtime graph docs | importante |
| worker WHY docs | importante |
| parser/scoring docs | importante |
| dashboard docs | importante |
| archives historiques | best effort |

## Regles

- Les surfaces critiques doivent exposer leurs invariants.
- Les surfaces runtime doivent exposer leurs classes R0-R5.
- Les surfaces critiques doivent exposer leurs reviews humaines.
- Les surfaces externes doivent rester contextualisees.

## Observation

Le lint doit prioriser:
- les surfaces critiques,
- les surfaces runtime,
- les surfaces multi-machine,
- les surfaces governance.

## Invariant

Le lint WHY ne doit jamais inferer une criticite runtime non documentee.
