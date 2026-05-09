# 80_RUNTIME_GRAPH_HUMAN_REVIEW_GATES

## Objectif

Relier les gates humaines au WHY runtime graph.

## Gates candidates

| Gate | Usage |
| --- | --- |
| RUNTIME_REVIEW_REQUIRED | runtime critique |
| OBSERVABILITY_REQUIRED | preuve runtime obligatoire |
| MULTI_MACHINE_REVIEW | orchestration distribuee |
| EXTERNAL_SURFACE_REVIEW | surface externe critique |
| GOVERNANCE_ALIGNMENT_REQUIRED | coherence WHY/runtime |

## Relations candidates

| Relation | Sens |
| --- | --- |
| REVIEWED_BY | review humaine associee |
| BLOCKED_BY | gate non satisfaite |
| VALIDATED_BY | preuve ou review validee |

## Regles

- Les surfaces critiques doivent garder review humaine.
- Les gates doivent etre explicables.
- Les validations doivent etre tracables.
- Les dependances critiques doivent etre visibles.

## Invariant

Le graphe ne doit jamais transformer une gate humaine en validation runtime autonome.
