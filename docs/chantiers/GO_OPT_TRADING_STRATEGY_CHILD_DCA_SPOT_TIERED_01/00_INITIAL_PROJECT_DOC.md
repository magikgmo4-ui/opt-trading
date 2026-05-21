---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DCA_SPOT_TIERED_01_INITIAL
doc_type: initial_project_doc
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DCA_SPOT_TIERED_01
status: open
updated_at: 2026-05-21
---

# GO_OPT_TRADING_STRATEGY_CHILD_DCA_SPOT_TIERED_01

## Concept

DCA spot à 3 couches avec amplification sur correction et rotation L1.

```
L0  Réserve liquide (staging)
L1  DCA base      — achat hebdo si prix < ref_W2, vente si prix > ref_W2 ou spike
L2  Accumulation M — achat amplifié si correction weekly ≥ seuil_M
L3  Accumulation G — achat amplifié si correction monthly ≥ seuil_G
```

## Règles

### Achat L1
- Fenêtre : 1 semaine max, 1 achat par semaine
- Trigger : low_D1 < ref_W2 (price dips below 2-week-ago reference)
- Entrée : limit à ref_W2 (pas au close — meilleur prix)
- Fallback : close du vendredi si aucun trigger dans la semaine

### Achat L2 / L3
- L2 : corr_4w_high ≤ -seuil_M%  (correction depuis le high des 4 semaines précédentes)
- L3 : corr_4m_high ≤ -seuil_G%  (correction depuis le high des 4 mois précédents)
- Cooldown L2 : 2 semaines min entre achats
- Cooldown L3 : 4 semaines min entre achats
- Entrée : close du bar déclenchant

### Vente L1 uniquement (FIFO)
- Prix   : high_D1 > ref_W2 → vente à ref_W2
- Spike  : (close - open) > spike_k × ATR_D1 → vente au close

### Capital
- Injection hebdo fixe : S (base unit)
- Nouveaux fonds → L0, déployés selon triggers
- Plafond : pas de limite dans v1 (mesurer l'exposition max)

## Paramètres à optimiser

| Param | Options |
|---|---|
| ref_type | w2_close / ma4w |
| seuil_M | 5 / 8 / 10 / 15 % |
| seuil_G | 15 / 20 / 30 % |
| mult_M | 2× / 3× / 5× |
| mult_G | 5× / 10× / 20× |
| sell_mode | price_only / price_or_spike |
| spike_k | 1.5 / 2.0 / 3.0 |

## Métriques cibles

- avg_entry_price < benchmark (simple weekly Monday open)
- total_return > benchmark
- max_simultaneous_capital : mesurer le pic d'exposition
- l1_rotation_rate : % des unités L1 vendues sur la période

## Critères d'acceptance

| Critère | Requis |
|---|---|
| avg_entry_price < benchmark | ✅ |
| total_return > benchmark | ✅ |
| L2/L3 déclenchent sur vraies corrections | ✅ |
| Pas de look-ahead | ✅ |

## Scope

- Crée : `tools/strategy/dca_spot/`
  - `indicators.py` — ref_W2, corr_4w, corr_4m, ATR, spike
  - `engine.py` — machine d'état L0/L1/L2/L3
  - `run_backtest.py` — simulation + benchmark comparaison
  - `run_optimization.py` — grid search 216+ combos
