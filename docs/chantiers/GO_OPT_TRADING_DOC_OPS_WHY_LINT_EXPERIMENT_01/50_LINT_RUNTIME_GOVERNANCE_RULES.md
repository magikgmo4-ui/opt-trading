# 50_LINT_RUNTIME_GOVERNANCE_RULES

## Objectif

Definir les regles runtime/governance du WHY lint experimental.

## Regles candidates

| Regle | Verification |
| --- | --- |
| invariant present | oui |
| runtime class exposee | oui |
| recovery path documente | oui |
| human review presente | oui |
| observabilite presente | oui |

## Surfaces critiques

Les surfaces:
- R4,
- R5,
- multi-machine,
- externes critiques,

doisvent augmenter la severite des warnings.

## Regles governance

- Les surfaces critiques doivent exposer leurs limites.
- Les reviews humaines doivent etre visibles.
- Les dependances critiques doivent etre documentees.
- Les incoherences runtime/governance doivent etre detectables.

## Invariant

Le lint WHY ne doit jamais devenir une validation runtime autonome.
