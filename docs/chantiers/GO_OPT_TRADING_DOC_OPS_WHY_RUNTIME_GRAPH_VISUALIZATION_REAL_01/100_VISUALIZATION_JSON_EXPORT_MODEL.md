# 100_VISUALIZATION_JSON_EXPORT_MODEL

## Objectif

Preparer le modele export JSON du WHY runtime graph.

## Structure candidate

| Champ | Usage |
| --- | --- |
| nodes | surfaces runtime/governance |
| edges | relations runtime |
| runtime_class | criticite R0-R5 |
| observability | preuves runtime |
| review_gates | validation humaine |
| recovery_paths | reprise runtime |
| machine_context | contexte multi-machine |

## Types candidats

| Type | Usage |
| --- | --- |
| WHY node | composant WHY |
| runtime node | surface runtime |
| machine node | machine |
| governance node | review humaine |
| observability node | preuves runtime |

## Regles

- Les exports doivent rester explicables.
- Les surfaces critiques doivent rester contextualisees.
- Les preuves runtime doivent rester tracables.
- Les validations humaines doivent rester visibles.

## Invariant

L'export JSON WHY runtime graph ne doit jamais devenir une API runtime autonome.
