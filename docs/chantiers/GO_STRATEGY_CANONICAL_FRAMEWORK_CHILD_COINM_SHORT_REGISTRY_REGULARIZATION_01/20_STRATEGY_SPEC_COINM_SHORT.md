---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_COINM_SHORT_REGISTRY_REGULARIZATION_01
doc_type: strategy_spec
---

# 20_STRATEGY_SPEC_COINM_SHORT

## Spec minimale

| Champ | Valeur |
|-------|--------|
| `strategy_id` | `COINM_SHORT` |
| `strategy_version` | `v0.1.0` |
| `family` | `trend_following` |
| `direction` | `SHORT` |
| `setup_type` | `lower_high_structure_ma_break` |
| `instruments` | `BTCUSDT.P`, `ETHUSDT.P` (COIN-M futures) |
| `timeframes` | `H1` (invalidation), `M15` (entry confirmation implicite) |

### Conditions d'entrée

1. Structure baissière : `lower_high` confirmé.
2. Prix sous MAs : `below_ma_50` ou `below_ma_100`.
3. Pas de macro haut-impact imminent.
4. Prix dans `entry_zone` définie.

### Invalidation

- `H1` close > `invalidation_level`.

### Take-profit

- 3 targets par position, définis dans CONFIG.

### Priorité

- Priorité #1 dans `pick_one_signal()` — passe avant GOLD_CFD_LONG et USDTM_LONG.

### Limites connues

- Pas de gestion de taille de position (risk sizing).
- Pas de trailing stop.
- Pas de ré-entrée après invalidation.
- `lower_low` non requis (`lower_low or True`).
- Pas de filtre volume ou RSI.

## RISKS

- À qualifier.
