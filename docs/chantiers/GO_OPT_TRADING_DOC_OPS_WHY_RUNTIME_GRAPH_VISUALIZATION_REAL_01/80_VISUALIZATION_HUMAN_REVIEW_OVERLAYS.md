# 80_VISUALIZATION_HUMAN_REVIEW_OVERLAYS

## Objectif

Formaliser les overlays review humaine du WHY runtime graph.

## Gates humaines candidates

| Gate | Usage |
| --- | --- |
| REVIEW_REQUIRED | validation humaine |
| RUNTIME_PROOF_REQUIRED | preuve runtime obligatoire |
| GOVERNANCE_ALIGNMENT_REQUIRED | coherence WHY/runtime |
| MULTI_MACHINE_REVIEW_REQUIRED | orchestration distribuee |

## Overlays candidats

| Overlay | Usage |
| --- | --- |
| review required | surfaces critiques |
| review status | validation humaine |
| governance alignment | coherence WHY/runtime |
| recovery validation | verification reprise |
| runtime proof validation | verification execution |

## Regles

- Les overlays review doivent rester explicables.
- Les surfaces critiques doivent garder validation humaine.
- Les preuves runtime doivent rester auditables.
- Les validations humaines doivent rester visibles.

## Invariant

Les overlays review humaine ne doivent jamais remplacer une validation humaine reelle.
