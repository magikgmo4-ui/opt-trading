---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01_ACCEPTANCE
doc_type: acceptance_report
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01
status: pending
updated_at: 2026-05-21
---

# 20_ACCEPTANCE_REPORT

**Statut : CLOSED — CHOCH fix livré, verdict stratégie = REJECT**

## Résultats backtest

```
Source données   : dukascopy 2024-01-01 → 2025-12-31 (140k barres M5)
confirm_window   : 5 barres

Avant rework :
  SMC_SWEEP_ONLY  : trades=19   exp=-0.56R  pf=0.338  winrate=15.8%
  COMBINED        : trades=6    exp=-0.07R  pf=0.9    winrate=33.3%

Après rework :
  SMC_SWEEP_ONLY  : trades=306  exp=-0.19R  pf=0.738  → REJECT_VARIANT
  COMBINED        : trades=37   exp=-0.39R  pf=0.497  → NEED_MORE_DATA

Verdict final    : REJECT — expectancy négative sur échantillon valide
```

## Critères

| Critère | Requis | Statut |
|---|---|---|
| SMC_SWEEP trades ≥ 100 | ✅ | ✅ 306 trades |
| Pas de look-ahead | ✅ | ✅ CHOCH cherché sur barres futures disponibles |
| Backtest sans crash | ✅ | ✅ |
| COMBINED trades ≥ 50 | ✅ | ❌ 37 (NEED_MORE_DATA) |

## Conclusion

Le fix CHOCH multi-bar est méthodologiquement correct et génère un échantillon valide (306 trades).
La stratégie SMC_ORB_VWAP_SCALP_A_PLUS a une **expectancy négative** sur données réelles XAUUSD.
Prochaine étape : GO_ENTRY_QUALITY_REWORK — revoir SL placement, TP targets, filtres de session.
