---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_STRATEGY_COMPARISON_MATRIX
doc_type: strategy_comparison_matrix
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: draft
lifecycle_stage: research
topic_keys: [opt-trading, strategy, daily_scalping, comparison_matrix]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/10_RESEARCH_SOURCES.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/30_SELECTED_ROUTINE.md
---

# 20_STRATEGY_COMPARISON_MATRIX

## Grille de score

Score sur 10, pondéré par cinq axes :

| Axe | Poids |
| --- | ---: |
| Evidence / backtest public | 2 |
| Facilité d'automatisation | 2 |
| Robustesse contre chop | 2 |
| Compatibilité XAU/BTC/indices | 2 |
| Gestion du risque claire | 2 |

## Matrice comparative

| Option | Score | Statut | Usage principal | Risque principal |
| --- | ---: | --- | --- | --- |
| ORB 5m / 15m + volume relatif | 9.0 | PRIORITY | indices, actions, XAU | faux breakout sans filtre |
| Intraday momentum + trailing/VWAP exit | 8.5 | PRIORITY | trend day, SPY/NQ/BTC | retournement brutal |
| VWAP pullback trend continuation | 8.0 | SUPPORT | XAU, indices, BTC | chop autour VWAP |
| SMC liquidity sweep + CHOCH/BOS/retest | 7.5 | SUPPORT_VISUAL | XAU, BTC, FX | subjectivité / surlecture |
| Donchian / breakout crypto trend | 7.0 | CRYPTO_VARIANT | BTC / majors crypto | whipsaw en range |
| Mean reversion VWAP/Bollinger | 6.0 | CONDITIONAL | range propre | mortel en trend day |
| News scalping | 5.0 | HIGH_VARIANCE | macro event | slippage / spread / exécution |
| Telegram signal-following brut | 3.0 | REJECT_RAW | aucun sans filtre | dépendance externe non prouvée |

## Verdict

La meilleure solution n'est pas une option isolée. La routine candidate retient :

```text
ORB = moteur mesurable
VWAP = filtre de régime
SMC/ICT = confirmation structurelle visuelle
Risk engine = condition d'autorisation
Journal = preuve d'apprentissage
```

## 13_ESTABLISHED

- ORB est le meilleur noyau à mesurer en premier.
- VWAP est nécessaire pour réduire les trades contre-régime.
- SMC/ICT ajoute une lecture utile des sweeps, CHOCH, BOS, retests.
- Mean reversion et news scalping restent secondaires tant que le coût d'exécution n'est pas prouvé.

## 14_HYPOTHESIS

- La routine combinée peut améliorer le ratio signal/bruit contre ORB only ou SMC only.

## 16_TODO

- Backtester ORB only, VWAP pullback, SMC sweep et routine combinée sur le même échantillon.
- Mesurer : winrate, expectancy R, max drawdown R, faux signaux, temps moyen en trade, sensibilité au spread.
