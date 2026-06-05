---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_USDTM_LONG_REGISTRY_REGULARIZATION_01
doc_type: strategy_spec
---

# 20_STRATEGY_SPEC_USDTM_LONG

## Spec minimale

| Champ | Valeur |
|-------|--------|
| `strategy_id` | `USDTM_LONG` |
| `strategy_version` | `v0.1.0` |
| `family` | `trend_following` |
| `direction` | `LONG` |
| `setup_type` | `bullish_confirmation_pullback` |
| `instruments` | `BTCUSDT.P` (USDT-M futures) |

### Conditions d'entrée

1. RSI > 50 rising.
2. Volume acheteur dominant.
3. Prix au-dessus MA50 et MA100.
4. Pas de macro haut-impact imminent.
5. BTC est leader (filtre `btc_is_leader`).
6. Prix dans pullback zone (`entry_zone`).

### Invalidation

- H1 close < `invalidation_level`.

### Take-profit

- 2 targets dans CONFIG.

### Priorité

- Priorité #3 dans `pick_one_signal()` — passe après COINM_SHORT et GOLD_CFD_LONG.

### Limites connues

- Pas de gestion de taille de position.
- Pas de trailing stop.
- Pas de ré-entrée après invalidation.
- 1 instrument seulement (BTC).
- Filtre `btc_is_leader` dur.

## RISKS

- À qualifier.
