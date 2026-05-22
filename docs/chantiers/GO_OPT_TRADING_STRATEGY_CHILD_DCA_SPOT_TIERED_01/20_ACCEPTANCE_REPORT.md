---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DCA_SPOT_TIERED_01_ACCEPTANCE
doc_type: acceptance_report
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DCA_SPOT_TIERED_01
status: closed
verdict: NON CONCLUANT
updated_at: 2026-05-21
---

# Acceptance Report — GO_OPT_TRADING_STRATEGY_CHILD_DCA_SPOT_TIERED_01

## Résumé

Trois variantes DCA spot backtestées sur deux périodes :
- **2024-2025** : XAUUSD M5 Dukascopy → D1 (625 barres, source broker)
- **2020-2023** : GC=F yfinance D1 (1006 barres, proxy spot — spread non utilisé)

Aucune variante ne bat le benchmark sur les deux métriques simultanément.
Le mécanisme de vente est structurellement incompatible avec un marché haussier.

---

## Benchmark

Simple DCA — achat 1S chaque lundi au Monday open.

| Période | avg_price | total_return |
|---|---|---|
| 2024-2025 | 2 909 pts | +48.5 % |
| 2020-2023 | 1 827 pts | +12.8 % |

---

## Variante 1 — DCA Étagé L0/L1/L2/L3

### Architecture

```
L0  Réserve (weekly_injection = 1S/semaine)
L1  Achat hebdo : low_D1 < ref_W2 → entrée à ref_W2 ; fallback Monday open
L2  Amplification : corr_4w ≤ seuil_M → achat mult_M × S
L3  Amplification : corr_4m ≤ seuil_G → achat mult_G × S
L1 sell : close > ref_W2 → vente au close (ou spike)
```

### Résultats grid (792 combos par période)

**Aucun combo ne bat le benchmark sur avg_price ET return simultanément.**

| Période | Meilleure config | avg_price | delta bench | return | delta bench |
|---|---|---|---|---|---|
| 2024-2025 | ma4w, corr_M=-15% (L2 inactif) | 2 908 | −0.87 ✅ | 46.1 % | −2.4 ❌ |
| 2020-2023 | ma4w, corr_M=-5%, mult_M=5× | 1 818 | −9.4 ✅ | 6.0 % | −6.8 ❌ |

### L3 — zéro déclenchement sur les deux périodes

- 2024-2025 : aucune correction ≥ 15% depuis le 4m-high
- 2020-2023 : COVID crash Gold = −12% (liquidité de crise, jamais −15%)
  → `mult_large` sans effet, paramètre inopérant sur ces données

---

## Variante 2 — DCA Adaptatif (×mult / ×frac)

### Règles

- Achat : `BASE_UNIT × buy_mult` si `close < last_buy_price`, sinon `BASE_UNIT`
- Vente FIFO : `BASE_UNIT × sell_frac` si `close > first_buy_price`
- Grid : freq ∈ {1,5,10,21} D1 bars × buy_mult ∈ {1.1,1.2,1.5,2.0} × sell_frac ∈ {0.5,0.8,1.0}

### Résultats — meilleur par fréquence (buy_mult=2.0, sell_frac=0.5 gagne toujours)

**2024-2025 :**

| Fréquence | avg_price | delta bench | return | delta bench |
|---|---|---|---|---|
| Monthly | 2 803 | −94 ✅ | 37.3 % | −11.8 ❌ |
| Weekly | 2 893 | −16 ✅ | 34.0 % | −15.0 ❌ |

**2020-2023 :**

| Fréquence | avg_price | delta bench | return | delta bench |
|---|---|---|---|---|
| Monthly | 1 815 | −6.6 ✅ | 9.4 % | −3.8 ❌ |
| Weekly | 1 824 | −3.6 ✅ | 8.8 % | −4.0 ❌ |

---

## Diagnostic structurel

**La règle de vente est le problème, pas les seuils de déclenchement.**

En marché haussier (les deux périodes testées), toute vente déploie des unités
au lieu de les accumuler. Net résultat : moins d'unités détenues à la clôture,
exposition réduite, return inférieur. L'amélioration sur avg_price est réelle
(−3 à −94 pts selon la fréquence) mais insuffisante pour compenser la réduction
d'exposition.

La stratégie serait performante sur un marché **range-bound** ou **bear-puis-bull** :
l'amélioration du prix d'accumulation + amplification dip se convertit en
outperformance quand le marché consolide avant une hausse.

---

## Vérification des critères d'acceptance

| Critère | 2024-2025 | 2020-2023 |
|---|---|---|
| avg_entry_price < benchmark | ✅ (adaptatif) | ✅ |
| total_return > benchmark | ❌ | ❌ |
| L2 déclenche sur vraies corrections | ✅ (étagé, −5%) | ✅ (30 fois) |
| L3 déclenche sur grandes corrections | ❌ (0 fois) | ❌ (0 fois, COVID −12%) |
| Pas de look-ahead | ✅ | ✅ |

---

## Verdict final : NON CONCLUANT

### Motif

XAUUSD est en tendance haussière structurelle 2020-2025.
Toute règle de vente conditionne la performance à une reprise post-consolidation
qui, dans les données disponibles, ne compense pas la perte d'exposition.

### Pivot recommandé

Remplacer la règle de vente par une **règle de réallocation** :
au lieu de vendre les unités L1 quand `close > ref_w2`, les recycler en L0
**uniquement si L2 ou L3 est sur le point de se déclencher** (capital disponible
pour amplifier la prochaine correction). Sans correction imminente, conserver.

Cela permettrait de cumuler l'avantage d'accumulation (avg_price inférieur)
sans réduire l'exposition en bull run.

### Réutilisation

`tools/strategy/dca_spot/` est prêt.
`data/market/xauusd_d1_2020_2023.csv` : 1006 barres GC=F D1 disponibles.
Extension minimale : modifier `engine.py` sell condition pour recycler
plutôt que réaliser.
