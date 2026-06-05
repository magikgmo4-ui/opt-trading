---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_BTC_COINM_ACCUMULATION_REGISTRY_REGULARIZATION_01
doc_type: strategy_spec
---

# 20_STRATEGY_SPEC_BTC_COINM_ACCUMULATION

## Spec minimale

| Champ | Valeur |
|-------|--------|
| `strategy_id` | `btc_coinm_accumulation` |
| `strategy_version` | `v0.1.0` |
| `family` | `accumulation` |
| `direction` | `LONG_SHORT` |
| `setup_type` | `dca_accumulation_hedge` |
| `instruments` | `BTC` (COIN-M) |

### Concept

DCA accumulation long + COIN-M shorts en couverture. Draft non implémenté.

### Limites

- Concept seulement, pas de logique de signal.
- Pas de runtime.
- Nécessite GO de validation avant implémentation.

## RISKS

- À qualifier.
