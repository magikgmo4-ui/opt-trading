# 110_STATIC_PROTOTYPE_JSON_EXPORT_PLAN

## Objectif

Preparer le premier export JSON reel du prototype WHY/runtime.

## Champs candidats

| Champ | Usage |
| --- | --- |
| nodes | surfaces runtime/governance |
| edges | relations runtime |
| runtime_class | criticite R0-R5 |
| overlays | contextualisation runtime |
| observability | preuves runtime |
| review_gates | validation humaine |
| machine_context | orchestration multi-machine |

## Formats candidats

| Format | Usage |
| --- | --- |
| graph json | export runtime graph |
| snapshot json | etat governance/runtime |
| metadata json | overlays runtime |

## Regles

- Les exports doivent rester explicables.
- Les surfaces critiques doivent rester contextualisees.
- Les validations humaines doivent rester visibles.
- Les exports doivent rester lecture seule.

## Invariant

Le JSON export WHY/runtime ne doit jamais devenir une API runtime autonome.
