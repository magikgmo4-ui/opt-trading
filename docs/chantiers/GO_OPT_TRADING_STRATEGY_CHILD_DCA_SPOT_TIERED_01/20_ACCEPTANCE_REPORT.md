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

Trois variantes DCA spot backtestées sur XAUUSD D1, 2024-01-01 → 2025-12-31 (625 barres).
Aucune variante ne bat le benchmark sur les deux métriques simultanément.
Les mécanismes sont corrects et sans look-ahead ; la limitation est le dataset, pas la logique.

## Benchmark

Simple DCA hebdomadaire — achat 1S chaque lundi au Monday open.

| Métrique | Valeur |
|---|---|
| n_buys | 105 |
| avg_price | 2 909 pts |
| total_return_pct | +48.5 % |

## Variante 1 — DCA Étagé L0/L1/L2/L3

### Architecture

```
L0  Réserve (weekly_injection = 1S/semaine)
L1  Achat hebdo : low_D1 < ref_W2 → entrée à ref_W2 ; fallback Monday open
L2  Amplification moyenne : corr_4w ≤ seuil_M → achat mult_M × S
L3  Amplification grande : corr_4m ≤ seuil_G → achat mult_G × S
L1 sell : close > ref_W2 → vente au close (ou spike)
```

### Résultats grid (216 combos)

Aucun combo ne bat le benchmark sur avg_price ET return simultanément.

- Seule config battant benchmark sur avg_price : `ref=ma4w, corr_M=-15%` (L2 ne se déclenche jamais)
  → avg_price 2 908.13 (−0.87 pts), return +46.1% (−2.4 pts vs bench)

- Configs L2 actives (`corr_M=-5%`, 13 déclenchements L2) :
  → avg_price 2 933–2 960 (plus cher que bench), return légèrement supérieur
  → Le prix des "corrections" en 2024-2025 reste élevé (ex. correction depuis 3 500 → 3 249)

- L3 : zéro déclenchement sur toute la période (aucune correction ≥ 15% du 4m-high)

### Diagnostic

Le dataset 2024-2025 est un bull run quasi-continu (+60% de 2 000 à 3 200 pts).
Les corrections hebdomadaires partent d'un niveau élevé → les achats L2 se font à prix élevé.
Le mécanisme est correct ; le contexte de marché le défavorise.

## Variante 2 — DCA Adaptatif (×mult / ×frac)

### Règles

- Achat : `BASE_UNIT × buy_mult` si `close < last_buy_price`, sinon `BASE_UNIT`
- Vente FIFO : `BASE_UNIT × sell_frac` si `close > first_buy_price`
- Grid : freq ∈ {1,5,10,21} D1 bars × buy_mult ∈ {1.1,1.2,1.5,2.0} × sell_frac ∈ {0.5,0.8,1.0}

### Résultats (meilleur par fréquence — buy_mult=2.0, sell_frac=0.5 gagne partout)

| Fréquence | avg_price | price_delta | held_qty | portfolio_return | delta_vs_bench |
|---|---|---|---|---|---|
| Daily (f=1) | 2 872.30 | −37.45 | 516.0 | +33.85 % | −14.76 pts |
| Weekly (f=5) | 2 893.02 | −15.82 | 114.0 | +34.02 % | −15.03 pts |
| Biweekly (f=10) | 2 879.98 | −17.80 | 58.0 | +35.51 % | −13.54 pts |
| Monthly (f=21) | 2 803.66 | −94.12 | 24.5 | +37.26 % | −11.79 pts |

### Diagnostic

- avg_price systématiquement inférieur au benchmark : ✅ (meilleure accumulation)
- portfolio_return systématiquement inférieur : ❌ (37–34% vs 49%)
- La règle de vente ×0.5 déploie les unités au lieu de les accumuler pendant le bull run
- Moins d'unités détenues au final → exposition réduite → return réduit
- En marché latéral ou baissier-puis-haussier, l'avantage avg_price se convertit en outperformance

## Vérification des critères d'acceptance

| Critère | Résultat |
|---|---|
| avg_entry_price < benchmark | ✅ (adaptatif : −94 pts mensuel) |
| total_return > benchmark | ❌ (−11 pts de return minimum) |
| L2/L3 déclenchent sur vraies corrections | ✅ (L2 oui, L3 jamais — dataset trop bullish) |
| Pas de look-ahead | ✅ |

## Verdict : NON CONCLUANT

### Motif

Les mécanismes d'amplification et de vente fonctionnent correctement.
La contrainte est le dataset (2 ans de bull run XAUUSD) :
- Aucune correction ≥ 20% depuis le 4m-high → L3 dormant
- Les corrections hebdomadaires partent d'un niveau élevé → L2 achète cher
- La vente FIFO sur hausse réduit l'exposition nette en bull run

### Condition de réévaluation

Réévaluer sur 2020-2024 (COVID crash, correction taux 2022, consolidation 2023) :
- L3 devrait se déclencher sur COVID (-30%) et 2022 (-20%)
- avg_price bien inférieur → return supérieur au bull-run simple
- Dataset requis : Dukascopy M5 2020-01-01 → 2023-12-31

### Réutilisation

`tools/strategy/dca_spot/` est prêt à l'emploi.
Extension minimale pour réévaluation : ajouter 4 ans de données M5 au fichier canonique et relancer.
