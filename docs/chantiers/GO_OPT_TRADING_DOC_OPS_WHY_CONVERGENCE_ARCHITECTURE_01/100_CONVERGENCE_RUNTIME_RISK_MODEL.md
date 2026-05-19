# 100_CONVERGENCE_RUNTIME_RISK_MODEL

## Objectif

Formaliser le modele de risque runtime WHY convergent.

## Facteurs de risque candidats

| Facteur | Impact |
| --- | --- |
| criticite R4/R5 | impact runtime eleve |
| orchestration multi-machine | propagation risques |
| observabilite absente | perte visibilite |
| review humaine absente | derive governance |
| recovery path absent | reprise incomplete |
| surfaces externes critiques | dependances externes |

## Relations candidates

| Source | Risque |
| --- | --- |
| runtime graph | propagation relations |
| lint experiment | detection gaps |
| score generator | maturite WHY faible |
| worker audit | aggregation risques |
| dashboard | visualisation risques |

## Regles

- Les surfaces critiques doivent augmenter la severite.
- Les risques doivent rester contextualises.
- Les preuves runtime doivent rester visibles.
- Les reviews humaines doivent rester obligatoires sur surfaces critiques.

## Invariant

Le modele de risque WHY ne doit jamais devenir un moteur de decision runtime autonome.
