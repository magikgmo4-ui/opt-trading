---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01_ACCEPTANCE
doc_type: acceptance_report
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01
status: pending
updated_at: 2026-05-21
---

# 20_ACCEPTANCE_REPORT

**Statut : CLOSED — fixes livrés, expectancy inversée**

## Baseline (avant rework)

```
SMC_SWEEP_ONLY  : trades=306  exp=-0.19R  pf=0.738  → REJECT_VARIANT
COMBINED        : trades=37   exp=-0.39R  pf=0.497  → NEED_MORE_DATA
```

## Résultats après rework

```
Données : dukascopy 2024-01-01 → 2025-12-31, 140k barres M5
Fixes   : SL ancré swept level + filtre sessions london/ny/overlap uniquement

SMC_SWEEP_ONLY  : trades=89   exp=+0.55R  pf=2.367  → NEED_MORE_DATA (< 100)
COMBINED        : trades=37   exp=+0.48R  pf=2.10   → NEED_MORE_DATA (< 100)
```

## Critères

| Critère | Requis | Statut |
|---|---|---|
| Expectancy > -0.10R | ✅ | ✅ +0.55R SMC, +0.48R COMBINED |
| Pas de look-ahead | ✅ | ✅ sweep_extreme = bar passée |
| Backtest sans crash | ✅ | ✅ |
| SMC_SWEEP trades ≥ 100 | ✅ | ❌ 89 — NEED_MORE_DATA |
| COMBINED trades ≥ 100 | ✅ | ❌ 37 — NEED_MORE_DATA |

## Conclusion

Signal fortement positif (+0.55R, PF 2.37). Seuil de 100 trades non atteint.
Prochaine étape : étendre données à 2023 (3 ans) ou ajuster confirm_window pour augmenter le sample.
