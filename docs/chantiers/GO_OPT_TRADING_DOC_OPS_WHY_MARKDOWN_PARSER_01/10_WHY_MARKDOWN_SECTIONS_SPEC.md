# 10_WHY_MARKDOWN_SECTIONS_SPEC

## Objectif

Formaliser les sections markdown que le futur parser WHY devra reconnaitre.

## Sections principales

| Section | Role | Criticite |
| --- | --- | --- |
| WHY | raison structurelle | haute |
| INVARIANTS | limites non negociables | haute |
| FAILURE_MODE | derive ou risque connu | haute |
| TRADEOFF | compromis accepte | moyenne |
| GATE | validation obligatoire | haute |
| RESUME_POINT | reprise operationnelle | haute |
| CANONICAL_STATE | etat valide courant | haute |
| FINAL_TARGET | livrable courant | moyenne |
| TODO | actions restantes | moyenne |

## Alias acceptes

| Canonique | Alias possibles |
| --- | --- |
| WHY | POURQUOI, RATIONALE, INTENTION |
| INVARIANTS | 12_INVARIANTS, CONTRAINTES |
| FAILURE_MODE | RISKS, RISK_AVOIDED, DERIVES |
| TRADEOFF | COMPROMIS, ARBITRAGE |
| GATE | PASS_FAIL, VALIDATION |
| RESUME_POINT | 17_RESUME_POINT, REPRISE |
| CANONICAL_STATE | 7_CANONICAL_STATE, ETAT_CANONIQUE |

## Regles de detection

- Detecter les headings markdown `#`, `##`, `###`.
- Normaliser les titres en majuscules sans accents pour comparaison.
- Conserver le titre original dans la sortie.
- Ne pas inferer une section absente.
- Ne pas fusionner deux sections differentes sans preuve textuelle.

## Invariant

Le parser doit lire et classifier. Il ne doit jamais modifier le document source.

## RISKS

- À qualifier.
