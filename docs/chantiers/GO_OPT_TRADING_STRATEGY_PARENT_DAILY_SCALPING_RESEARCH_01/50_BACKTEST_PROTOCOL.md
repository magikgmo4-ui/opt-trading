---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_BACKTEST_PROTOCOL
doc_type: backtest_protocol
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01
chantier_parent: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: draft
lifecycle_stage: strategy_candidate
topic_keys: [opt-trading, strategy, daily_scalping, backtest, protocol]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/30_SELECTED_ROUTINE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/60_JOURNAL_TEMPLATE.md
---

# 50_BACKTEST_PROTOCOL

## Objectif

Tester la routine candidate `SMC_ORB_VWAP_SCALP_A_PLUS` avant toute promotion runtime.

## Périmètre V1

| Champ | Valeur |
| --- | --- |
| Marché initial | XAUUSD |
| Timeframes | M15 contexte, M5 exécution |
| Sessions | London open, NY open, overlap |
| Échantillon minimal | 100 occurrences |
| Échantillon cible | 300 occurrences |
| Mode | bar replay / historique, sans lookahead |
| Coûts | spread + commission + slippage simulé |

## Variants à comparer

| Variant | Description |
| --- | --- |
| ORB_ONLY | Opening range breakout/retest sans SMC ni VWAP avancé |
| VWAP_PULLBACK_ONLY | pullback VWAP avec biais session |
| SMC_SWEEP_ONLY | sweep + CHOCH/BOS + retest sans ORB |
| COMBINED | ORB/liquidity + VWAP + SMC + risk score |

## Métriques obligatoires

```text
trades_count
winrate
avg_win_R
avg_loss_R
expectancy_R
profit_factor
max_drawdown_R
max_losing_streak
avg_time_in_trade
false_signal_rate
missed_trade_rate
spread_sensitivity
score_bucket_performance
```

## Règles anti-biais

- Capturer le screenshot avant décision.
- Ne pas déplacer l'entrée après résultat connu.
- Ne pas supprimer les perdants du dataset.
- Ne pas mélanger les sessions sans étiquette.
- Ne pas mélanger XAUUSD, BTC et indices dans une même statistique V1.
- Garder les trades refusés dans un onglet `WATCH_REJECTED`.

## Critères de promotion

| Critère | Seuil initial |
| --- | ---: |
| Occurrences | >= 100 |
| Expectancy | > +0.15R |
| Profit factor | > 1.25 |
| Max drawdown | acceptable vs risk cap |
| Score >= 7 supérieur à score < 7 | obligatoire |
| Résultat stable par session | souhaité |

## Verdicts possibles

```text
PROMOTE_TO_PAPER_FORWARD
REWORK_RULESET
REJECT_VARIANT
NEED_MORE_DATA
```

## 13_ESTABLISHED

Aucune promotion runtime n'est autorisée sans résultat backtest documenté.

## 14_HYPOTHESIS

Le variant `COMBINED` devrait réduire les faux breakouts et les entrées en chop VWAP.

## 16_TODO

- Créer ou connecter un journal Google Sheets.
- Alimenter au moins 100 lignes XAUUSD.
- Produire un rapport `BACKTEST_VERDICT_01`.
