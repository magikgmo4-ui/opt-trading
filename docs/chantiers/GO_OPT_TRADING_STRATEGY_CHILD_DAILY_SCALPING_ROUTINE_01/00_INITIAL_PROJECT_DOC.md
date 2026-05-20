---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01
chantier_parent: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
lifecycle_stage: backtest
topic_keys:
  - opt-trading
  - strategy
  - daily_scalping
  - backtest
  - SMC_ORB_VWAP_SCALP_A_PLUS
  - XAUUSD
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/30_SELECTED_ROUTINE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/40_SIGNAL_SCHEMA.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/50_BACKTEST_PROTOCOL.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/60_JOURNAL_TEMPLATE.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Exécuter le backtest comparatif de la routine `SMC_ORB_VWAP_SCALP_A_PLUS` sur XAUUSD M5/M15,
produire le verdict et décider de la promotion.

## 3_INITIAL_NEED

Le parent a cadré et sélectionné la routine candidate. Ce child exécute le protocole :
100 occurrences minimum XAUUSD, 4 variants comparés, verdict documenté.

## 4_MASTER_PROJECT_PLAN

- Parent : `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`
- Ce child : backtest + verdict
- Routine : `SMC_ORB_VWAP_SCALP_A_PLUS`
- Marché V1 : XAUUSD M15 contexte / M5 exécution
- Sessions : London open, NY open, overlap

## 5_GO_PLAN

1. Alimenter le journal backtest — 100 occurrences minimum XAUUSD.
2. Comparer les 4 variants : `ORB_ONLY`, `VWAP_PULLBACK_ONLY`, `SMC_SWEEP_ONLY`, `COMBINED`.
3. Calculer les métriques obligatoires par variant.
4. Produire `BACKTEST_VERDICT_01`.
5. Décider la promotion.

## 6_SCOPE_LIMITS

- Pas d'automatisation avant verdict PASS.
- Pas de paper forward avant verdict PASS.
- Pas de live avant paper forward validé.
- Pas de code trading dans ce GO.
- Screenshots obligatoires avant/après chaque trade.

## 7_VERDICTS_POSSIBLES

```text
PROMOTE_TO_PAPER_FORWARD
REWORK_RULESET
REJECT_VARIANT
NEED_MORE_DATA
```

## 8_CRITERES_PROMOTION

| Critère | Seuil |
|---|---:|
| Occurrences | >= 100 |
| Expectancy | > +0.15R |
| Profit factor | > 1.25 |
| Score >= 7 supérieur à score < 7 | obligatoire |

## 13_ESTABLISHED

- Protocole backtest : `50_BACKTEST_PROTOCOL.md` du parent.
- Journal template : `60_JOURNAL_TEMPLATE.md` du parent.
- Règles anti-biais obligatoires.

## 16_TODO

1. Alimenter `10_BACKTEST_JOURNAL.md` — 100 trades XAUUSD.
2. Remplir `20_RESULTS_BY_VARIANT.md` — métriques par variant.
3. Produire `30_BACKTEST_VERDICT_01.md`.
4. Rédiger `90_REPRISE.md` closeout avec verdict final.
