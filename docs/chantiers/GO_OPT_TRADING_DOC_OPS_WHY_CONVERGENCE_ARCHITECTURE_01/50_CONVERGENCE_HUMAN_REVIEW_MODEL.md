# 50_CONVERGENCE_HUMAN_REVIEW_MODEL

## Objectif

Formaliser la gouvernance review humaine dans la convergence WHY.

## Role de la review humaine

La review humaine reste l'autorite finale pour:
- surfaces R4/R5,
- runtime critique,
- orchestration multi-machine,
- promotions de criticite,
- decisions d'implementation reelle.

## Relations avec les composants WHY

| Composant | Role review |
| --- | --- |
| parser WHY | detecte structure documentaire |
| score generator | indique maturite WHY |
| worker audit | prepare paquet review |
| runtime graph | expose relations critiques |
| dashboard | visualise risques et gaps |
| lint experiment | signale warnings |

## Gates humaines candidates

| Gate | Usage |
| --- | --- |
| REVIEW_REQUIRED | surface critique |
| RUNTIME_PROOF_REQUIRED | preuve runtime obligatoire |
| GOVERNANCE_ALIGNMENT_REQUIRED | coherence WHY/runtime |
| MULTI_MACHINE_REVIEW_REQUIRED | orchestration distribuee |

## Invariant

Aucun composant WHY ne doit remplacer une decision humaine sur surface critique.

## RISKS

- À qualifier.
