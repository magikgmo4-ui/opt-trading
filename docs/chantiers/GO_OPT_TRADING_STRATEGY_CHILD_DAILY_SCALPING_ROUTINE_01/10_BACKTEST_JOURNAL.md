---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01_BACKTEST_JOURNAL
doc_type: backtest_journal
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01
status: open
lifecycle_stage: backtest
topic_keys: [opt-trading, strategy, daily_scalping, backtest, XAUUSD, journal]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 10_BACKTEST_JOURNAL

## Marché / Périmètre

| Champ | Valeur |
|---|---|
| Marché | XAUUSD |
| Timeframe contexte | M15 |
| Timeframe exécution | M5 |
| Sessions | London open, NY open, overlap |
| Cible | 100 occurrences minimum |
| Mode | bar replay / historique, sans lookahead |

## Variants suivis

| Code | Description |
|---|---|
| `ORB_ONLY` | Opening range breakout/retest sans SMC ni VWAP avancé |
| `VWAP_PULLBACK_ONLY` | Pullback VWAP avec biais session |
| `SMC_SWEEP_ONLY` | Sweep + CHOCH/BOS + retest sans ORB |
| `COMBINED` | ORB/liquidity + VWAP + SMC + risk score |

## Journal (à alimenter)

| # | date | session | variant | direction | setup_score | entry_price | sl | tp1 | tp2 | result_R | followed_plan | notes |
|---|---|---|---|---|---:|---|---|---|---|---:|---|---|
| 1 | | | | | | | | | | | | |

> Utiliser les colonnes complètes du template parent (`60_JOURNAL_TEMPLATE.md`) dans Google Sheets.
> Ce fichier contient le résumé léger ; le journal complet vit dans Sheets.

## Règles anti-biais

- Screenshot avant décision obligatoire.
- Ne pas déplacer l'entrée après résultat connu.
- Ne pas supprimer les perdants.
- Trades refusés dans onglet `WATCH_REJECTED`.
- Ne pas mélanger les sessions sans étiquette.

## Progression

| Métrique | Valeur |
|---|---|
| Occurrences saisies | 0 / 100 |
| Variants couverts | 0 / 4 |
| Sessions couvertes | 0 / 3 |
