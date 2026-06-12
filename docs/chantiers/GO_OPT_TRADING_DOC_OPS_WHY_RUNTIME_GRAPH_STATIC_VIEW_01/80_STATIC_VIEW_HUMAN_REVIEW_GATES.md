# 80_STATIC_VIEW_HUMAN_REVIEW_GATES

## Objectif

Formaliser les gates review humaine de la vue statique WHY/runtime.

## Gates candidates

| Gate | Usage |
| --- | --- |
| REVIEW_REQUIRED | validation humaine |
| RUNTIME_PROOF_REQUIRED | preuve runtime obligatoire |
| GOVERNANCE_ALIGNMENT_REQUIRED | coherence WHY/runtime |
| MULTI_MACHINE_REVIEW_REQUIRED | orchestration distribuee |

## Overlays review

| Overlay | Usage |
| --- | --- |
| review required | surfaces critiques |
| review status | validation humaine |
| governance alignment | coherence WHY/runtime |
| runtime proof validation | verification execution |

## Regles

- Les surfaces critiques doivent garder validation humaine.
- Les preuves runtime doivent rester auditables.
- Les overlays review doivent rester explicables.
- Les validations humaines doivent rester visibles.

## Invariant

La vue WHY/runtime ne doit jamais remplacer une validation humaine critique.

## RISKS

- À qualifier.
