---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: reference
lifecycle_stage: research
topic_keys:
  - opt-trading
  - strategy
  - daily_scalping
  - scalping_routine
  - ORB
  - VWAP
  - SMC_ICT
  - risk_engine
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/70_RESUME_POINT.md
updated_at: 2026-05-20
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/10_RESEARCH_SOURCES.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/20_STRATEGY_COMPARISON_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/30_SELECTED_ROUTINE.md
  - docs/index/inbox/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01.md
---

# GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Créer un chantier indépendant de la session pour comparer les options de daily scalping et stabiliser une routine robuste compatible avec TradingView, screener headless, Telegram, bot vision, DeskPro, perf engine et journal Google Sheets.

## 2_INITIAL_PROJECT_DOC

Document transporteur initial du chantier. Il fige la demande, la direction, les GO rattachés, les invariants et le point de reprise.

## 3_INITIAL_NEED

Demande originale : rechercher plus profondément les meilleures stratégies de daily scalping, mesurer les options, puis créer le chantier, la documentation et les GO indépendamment de la session active.

## 4_MASTER_PROJECT_PLAN

- Parent : `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`.
- Child fonctionnel : `GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01`.
- Routine candidate retenue : `SMC_ORB_VWAP_SCALP_A_PLUS`.
- Nature : doc-only research + cadrage stratégie + protocole backtest.
- Indexation : entrée courte dans `docs/index/inbox/`, sans modification des index globaux.

## 5_GO_PLAN

1. Recenser les familles scalping pertinentes.
2. Comparer leur robustesse : evidence, automatisabilité, risque de chop, compatibilité marchés, risk engine.
3. Sélectionner une routine candidate.
4. Définir schéma signal, protocole backtest et journal.
5. Laisser l'exécution et l'automatisation hors scope tant que le backtest n'est pas validé.

## 6_FINAL_TARGET

Livrer une documentation canonique minimale permettant de reprendre le travail sans la conversation : sources, matrice de comparaison, routine sélectionnée, schéma signal, protocole de backtest, template journal et point de reprise.

## 7_CANONICAL_STATE

- Statut : `OPEN / DOC_ONLY`.
- Aucun ordre réel.
- Aucune automatisation d'exécution.
- Aucun index global modifié.
- Continuité locale portée par ce dossier parent et par l'entrée inbox atomique.

## 8_VALIDATED_PLAN

Fichiers du chantier :
- `00_INITIAL_PROJECT_DOC.md`
- `10_RESEARCH_SOURCES.md`
- `20_STRATEGY_COMPARISON_MATRIX.md`
- `30_SELECTED_ROUTINE.md`
- `40_SIGNAL_SCHEMA.md`
- `50_BACKTEST_PROTOCOL.md`
- `60_JOURNAL_TEMPLATE.md`
- `70_RESUME_POINT.md`

## 9_SELECTED_SOLUTION

Routine prioritaire à tester : `SMC_ORB_VWAP_SCALP_A_PLUS`.

Structure :

```text
HTF bias -> session filter -> opening range / liquidity zone -> sweep or breakout -> CHOCH/BOS -> VWAP regime filter -> retest -> entry -> partial TP -> journal -> review J+1
```

## 10_SELECTED_SETUP

- ORB = noyau le plus mesurable.
- VWAP = filtre de régime intraday.
- SMC/ICT = confirmation structurelle et langage visuel pour screenshots.
- Risk engine = condition d'existence de la routine.

## 11_KEY_DECISIONS

- Ne pas documenter une stratégie miracle.
- Ne pas exécuter des signaux Telegram bruts.
- Ne pas promouvoir SMC/ICT comme preuve statistique autonome.
- Backtest obligatoire avant toute automation.
- Score minimum d'entrée : 7/10.

## 12_INVARIANTS

- Aucun trade sans invalidation.
- Aucun trade sans RR minimum.
- Aucun trade après perte max journalière.
- Aucun signal externe exécuté sans recroisement.
- Aucun passage live avant backtest + paper forward.

## 13_ESTABLISHED

- ORB et momentum intraday sont les familles les plus mesurables.
- VWAP est utile comme filtre, pas comme signal autonome.
- SMC/ICT est utile pour qualifier structure, sweep, CHOCH, BOS et retest.
- Le scalping robuste dépend fortement des coûts, du spread, du slippage et du levier.

## 14_HYPOTHESIS

- `SMC_ORB_VWAP_SCALP_A_PLUS` peut produire une routine plus robuste que chaque famille isolée.
- XAUUSD M5/M15 est le premier terrain naturel de test.
- BTC perps doit utiliser un variant plus momentum / Donchian / liquidation zones.

## 15_REMAINING_GAP

- Backtest non encore réalisé.
- Données réelles de coûts/spread/slippage par broker non encore intégrées.
- Seuils de scoring à calibrer par marché.

## 16_TODO

1. Backtester 100 occurrences XAUUSD M5/M15.
2. Comparer ORB only, SMC only, VWAP pullback et routine combinée.
3. Remplir le journal.
4. Produire un verdict `PROMOTE / REWORK / REJECT`.

## 17_RESUME_POINT

Reprendre par `70_RESUME_POINT.md`, puis exécuter `50_BACKTEST_PROTOCOL.md` sur XAUUSD.

## 18_TO_DOCUMENT

- Résultats backtest.
- Ajustement scoring.
- Marchés compatibles.
- Version candidate runtime si validée.

## 19_TO_REMEMBER

### MEM_CANDIDATE

- Daily scalping robuste = ORB mesurable + VWAP filtre + SMC confirmation + risk engine + journalisation.

### SAVE_MEMORY

- Routine candidate prioritaire : `SMC_ORB_VWAP_SCALP_A_PLUS` pour test initial doc-only/backtest, sans exécution réelle.
