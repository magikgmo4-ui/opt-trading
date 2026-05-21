---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01_ACCEPTANCE
doc_type: acceptance_report
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ENTRY_QUALITY_REWORK_01
status: pending
updated_at: 2026-05-21
---

# 20_ACCEPTANCE_REPORT

**Statut : CLOSED — fixes livrés, résultats honnêtes documentés**

## Baseline (avant rework)

```
SMC_SWEEP_ONLY  : trades=306  exp=-0.19R  pf=0.738  → REJECT_VARIANT
COMBINED        : trades=37   exp=-0.39R  pf=0.497  → NEED_MORE_DATA
```

## Résultats après rework (v2 — RR cohérent)

```
Données : dukascopy 2024-01-01 → 2025-12-31, 140k barres M5
Fixes   :
  1. SL = swept_structure - 0.1×ATR (niveau structurel)
  2. TP = entry + risk × 1.8 (proportionnel au risque réel)
  3. result_R = abs(tp1-entry)/risk (corrige bug result_R hardcodé)
  4. Filtre sessions : london/ny/overlap pour SMC/COMBINED
  5. max_risk_atr=3.0 (rejette trades avec SL trop large)

SMC_SWEEP_ONLY  : trades=73   exp=-0.28R  pf=0.583  → NEED_MORE_DATA
COMBINED        : trades=30   exp=-0.10R  pf=0.848  → NEED_MORE_DATA

Note v1 invalide : exp=+0.55R reporté était bugué (result_R=1.8 hardcodé
sur TP, indépendamment du risque réel). Corrigé ici.
```

## Performance par session (v2)

| Session | Trades | WR | Exp | Breakeven 1.8:1 |
|---|---|---|---|---|
| overlap | 30 | 37% | +0.04R | 35.7% — marginal ✅ |
| ny | 44 | 34% | -0.25R | 35.7% — 1.7% sous |
| london | 29 | 17% | -0.47R | 35.7% — séance ouverture ❌ |

## Critères

| Critère | Requis | Statut |
|---|---|---|
| Pas de look-ahead | ✅ | ✅ |
| Backtest sans crash | ✅ | ✅ |
| result_R cohérent avec RR réel | ✅ | ✅ corrigé |
| Expectancy > 0R | cible | ❌ -0.28R SMC, -0.10R COMBINED |

## Conclusion

Le bug result_R était masqué par l'artefact de simulation.
La vraie performance est légèrement négative. Cause profonde : entry au close du
CHOCH bar = entrée trop tardive, loin de la structure.

Prochaine étape : GO_PULLBACK_ENTRY_01 — entrer sur pullback au swing_h (CHOCH level)
plutôt qu'au close de la barre de confirmation.
