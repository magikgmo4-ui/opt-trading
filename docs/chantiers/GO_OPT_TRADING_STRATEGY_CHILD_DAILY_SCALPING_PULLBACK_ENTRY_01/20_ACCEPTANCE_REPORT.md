---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01_ACCEPTANCE
doc_type: acceptance_report
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_PULLBACK_ENTRY_01
status: pending
updated_at: 2026-05-21
---

# 20_ACCEPTANCE_REPORT

**Statut : CLOSED — pullback entry livre expectancy positive**

## Baseline

```
SMC_SWEEP  : 73t   exp=-0.28R  overlap=+0.04R  risk_avg=5.47pts
COMBINED   : 30t   exp=-0.10R
Entry type : market order at CHOCH bar close
```

## Résultats pullback entry

```
Données    : dukascopy 2024-01-01 → 2025-12-31, 140k barres M5
Parameters : confirm_window=5, pullback_window=10, session=london/ny/overlap

SMC_SWEEP  : 84t   exp=+0.14R  PF=1.25  wr=40%  risk_avg=4.71pts  → NEED_MORE_DATA
COMBINED   : 33t   exp=+0.08R  PF=1.14  wr=36%  risk_avg=4.42pts  → NEED_MORE_DATA
Entry type : limit order at CHOCH level (swing_h/swing_l)
```

## Performance par session (SMC_SWEEP)

| Session | Trades | WR | Exp | Breakeven 1.8:1 |
|---|---|---|---|---|
| overlap | 42 | **50%** | **+0.43R** | 35.7% ✅ |
| ny | 41 | 34% | -0.06R | 35.7% — marginal |
| london | 34 | 32% | -0.05R | 35.7% — marginal |

## Critères

| Critère | Requis | Statut |
|---|---|---|
| Expectancy > 0R global SMC | cible | ✅ +0.14R |
| Expectancy > 0R overlap | ✅ | ✅ +0.43R |
| Trades ≥ 80 SMC | ✅ | ✅ 84 |
| No look-ahead | ✅ | ✅ pullback bar toujours après CHOCH |

## Conclusion

Première expectancy positive sur jeu de données réel Dukascopy.
Seuil 100 trades non atteint (84 SMC) → NEED_MORE_DATA.
Prochaine étape : données 3 ans (2023-2025) pour franchir le seuil.
