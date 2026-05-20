---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_JOURNAL_TEMPLATE
doc_type: journal_template
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01
chantier_parent: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: draft
lifecycle_stage: strategy_candidate
topic_keys: [opt-trading, strategy, daily_scalping, journal, google_sheets]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/50_BACKTEST_PROTOCOL.md
---

# 60_JOURNAL_TEMPLATE

## Objectif

Définir le journal minimal pour backtest, paper forward et revue J+1.

## Colonnes minimales

- date
- symbol
- market_type
- session
- timeframe_context
- timeframe_entry
- strategy_id
- variant
- direction
- bias_htf
- setup_type
- orb_state
- vwap_state
- liquidity_state
- structure_state
- entry_state
- entry_price
- stop_loss
- tp1
- tp2
- risk_pct
- rr_planned
- setup_score
- risk_status
- block_reason
- screenshot_before
- screenshot_after
- result_R
- mae_R
- mfe_R
- time_in_trade_minutes
- followed_plan
- mistake_tag
- notes
- review_j1
- verdict

## Tags de revue

Les erreurs, écarts et refus doivent être normalisés dans `mistake_tag` et `verdict` afin de permettre une mesure par type de setup, session, score et régime VWAP.

## Revue J+1

Questions obligatoires :

- Le setup était-il prévu avant la session ?
- Le score était-il supérieur ou égal à 7 ?
- Le trade respectait-il le régime VWAP ?
- L'invalidation était-elle structurelle ?
- Le ratio risque/rendement était-il suffisant ?
- La sortie était-elle conforme au plan ?

## 13_ESTABLISHED

Le journal est obligatoire pour toute promotion de stratégie.

## 16_TODO

- Créer une version Google Sheets calculée.
- Ajouter formules expectancy, profit factor, score bucket et session bucket.
