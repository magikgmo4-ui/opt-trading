# 90_EXTERNAL_SURFACES_RUNTIME_ALIGNMENT

## Objectif

Aligner les surfaces externes candidates avec la classification runtime R0-R5.

## Alignement candidat

| Surface | Classe candidate | Justification |
| --- | --- | --- |
| ClickUp | R2/R3 | suivi et propagation de statut |
| Botpress | R3 | orchestration conversationnelle |
| Knowledge Graph | R3 | relations et coherence projet |
| Airtable | R2/R3 | operations structurees |

## Regles

- Une surface externe reste R2 si elle observe ou structure seulement.
- Une surface externe devient R3 si elle influence une orchestration multi-machine.
- Une surface externe ne doit jamais devenir R4/R5 sans governance explicite.
- Toute promotion de criticite doit etre justifiee par preuve documentaire.

## Alignements WHY

| Classe | Exigence |
| --- | --- |
| R2 | observabilite et reprise recommandees |
| R3 | invariants, gates et review humaine |
| R4 | runtime critique, hors scope initial |
| R5 | interdit sans governance maximale |

## Invariant

La classe runtime d'une surface externe ne doit jamais etre inferee sans preuve explicite.
