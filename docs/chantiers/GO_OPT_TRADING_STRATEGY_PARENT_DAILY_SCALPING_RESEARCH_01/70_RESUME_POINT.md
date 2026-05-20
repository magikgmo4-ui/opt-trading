---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_RESUME_POINT
doc_type: resume_point
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: draft
lifecycle_stage: research
topic_keys: [opt-trading, strategy, daily_scalping, resume_point]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/50_BACKTEST_PROTOCOL.md
---

# 70_RESUME_POINT

## 7_CANONICAL_STATE

Chantier parent ouvert en doc-only pour comparer et stabiliser une routine daily scalping robuste.

## 1_MASTER_TARGET

Routine scalping robuste, mesurable et compatible stack opt-trading.

## 2_INITIAL_PROJECT_DOC

Référence : `00_INITIAL_PROJECT_DOC.md`.

## 4_MASTER_PROJECT_PLAN

- Parent : `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`.
- Child : `GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01`.
- Routine candidate : `SMC_ORB_VWAP_SCALP_A_PLUS`.

## 5_GO_PLAN

Exécuter le backtest comparatif : ORB only, VWAP only, SMC sweep only, combined.

## 6_FINAL_TARGET

Produire un verdict de promotion : `PROMOTE_TO_PAPER_FORWARD`, `REWORK_RULESET`, `REJECT_VARIANT` ou `NEED_MORE_DATA`.

## 13_ESTABLISHED

- ORB = noyau prioritaire mesurable.
- VWAP = filtre de régime.
- SMC/ICT = confirmation structurelle.
- Backtest obligatoire.

## 14_HYPOTHESIS

La routine combinée peut réduire les faux signaux par rapport à chaque méthode isolée.

## 15_REMAINING_GAP

Aucun backtest local encore documenté.

## 16_TODO

1. Créer ou connecter le journal Google Sheets.
2. Backtester 100 occurrences XAUUSD M5/M15.
3. Produire `BACKTEST_VERDICT_01`.
4. Décider si la stratégie devient candidate paper forward.

## 17_RESUME_POINT

Reprendre directement dans `50_BACKTEST_PROTOCOL.md`, avec XAUUSD M5/M15 comme premier marché.
