---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01_INITIAL
doc_type: initial_project_doc
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
updated_at: 2026-05-21
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_CHOCH_MULTI_BAR_REWORK_01

## Problème

Le backtest canonique Dukascopy 2024-01-01→2025-12-31 (140k barres M5) produit seulement **25 trades SMC** en 2 ans.

Cause racine : `detectors.py` exige que le CHOCH (Change of Character) soit confirmé **dans la même barre M5** que la récupération du sweep.

```python
# Ligne 110 — condition actuelle (trop stricte)
swept = prev["low"] < swing_l and row["close"] > swing_l   # récupération bar i
if swept and swing_h is not None and row["close"] > swing_h:  # CHOCH doit aussi être bar i
```

Sur M5, cette double condition (sweep + CHOCH dans 1 barre) exige un move de 15-20+ points, ce qui n'arrive que 25x en 2 ans.

## Objectif

Implémenter une **fenêtre de confirmation CHOCH** de 0-5 barres après la barre de récupération du sweep.

- Sweep détecté : bar[i-1] sweeps swing, bar[i] close au-delà du swept level
- CHOCH cherché : bar[i] → bar[i+5], premier bar dont close > swing_h (long) / < swing_l (short)
- Entry : bar du CHOCH confirmé

## Critères d'acceptance

| Critère | Attendu |
|---|---|
| SMC_SWEEP_ONLY trades ≥ 100 sur 2 ans | ✅ |
| COMBINED_SMC_ORB_VWAP trades ≥ 50 | ✅ |
| Backtest s'exécute sans crash | ✅ |
| Pas de look-ahead (CHOCH bar ≤ i+5 avec données disponibles) | ✅ |
| Logique k=0 ≡ comportement original | ✅ |

## Scope

- **Modifie** : `tools/strategy/daily_scalping/detectors.py`
- **Lit** : `data/market/xauusd_m5_canonical.csv` + M15
- **Produit** : verdict backtest dans `artifacts/backtests/daily_scalping_choch_rework/`
