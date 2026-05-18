---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_GOLD_CFD_LONG_REGISTRY_REGULARIZATION_01
doc_type: strategy_spec
---

# 20_STRATEGY_SPEC_GOLD_CFD_LONG

## Spec minimale

| Champ | Valeur |
|-------|--------|
| `strategy_id` | `GOLD_CFD_LONG` |
| `strategy_version` | `v0.1.0` |
| `family` | `trend_following` |
| `direction` | `LONG` |
| `setup_type` | `hl_structure_ma_buy` |
| `instruments` | `XAUUSD` (gold CFD) |

### Conditions d'entrée

1. Structure haussière : `higher_low`.
2. Prix au-dessus MA50.
3. Pas de macro haut-impact imminent.
4. Prix dans `entry_zone`.

### Invalidation

- M15 close < `invalidation_level`.

### Take-profit

- 3 targets dans CONFIG.

### Priorité

- Priorité #2 dans `pick_one_signal()` — passe après COINM_SHORT, avant USDTM_LONG.

### Limites connues

- 1 instrument (XAUUSD).
- Pas de trailing stop, pas de risk sizing.
- M15 invalidation seulement (timeframe court).
