# 100_STATIC_VIEW_JSON_EXPORT_ALIGNMENT_V2

## Objectif

Aligner la vue statique WHY/runtime avec le futur export JSON reel.

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

## Regles

- Les exports doivent rester explicables.
- Les surfaces critiques doivent rester contextualisees.
- Les validations humaines doivent rester visibles.
- Les exports doivent rester lecture seule.

## Formats candidats

| Format | Usage |
| --- | --- |
| graph json | export runtime graph |
| overlay json | contextualisation runtime |
| governance snapshot json | review humaine |

## Invariant

L'alignement JSON WHY/runtime ne doit jamais devenir une API runtime autonome.
