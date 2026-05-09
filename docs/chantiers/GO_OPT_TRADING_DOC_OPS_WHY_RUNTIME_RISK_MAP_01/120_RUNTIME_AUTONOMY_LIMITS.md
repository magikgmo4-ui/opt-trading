# 120_RUNTIME_AUTONOMY_LIMITS

## Objectif

Documenter les limites d'autonomie IA/runtime.

## Principes

Une IA peut:
- proposer,
- analyser,
- auditer,
- scorer,
- cartographier.

Mais les surfaces critiques doivent conserver des gates humaines.

## Limites critiques

| Surface | Limite |
| --- | --- |
| R0 | autonomie acceptable |
| R1 | autonomie faible risque |
| R2 | supervision recommandee |
| R3 | validation humaine recommandee |
| R4 | validation humaine obligatoire |
| R5 | autonomie interdite sans governance forte |

## Cas interdits

- execution financiere autonome sans gates,
- runtime critique sans observabilite,
- orchestration multi-machine non revue,
- modifications live sans reprise,
- application runtime sans verification.

## Observation

Le WHY layer existe pour:
- limiter les derives autonomes,
- ralentir les erreurs critiques,
- proteger la coherence operatoire.

## Invariant

Les surfaces R4/R5 ne devraient jamais dependre uniquement d'une logique autonome IA.
