---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01
chantier_parent: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
lifecycle_stage: automation
topic_keys:
  - opt-trading
  - strategy
  - daily_scalping
  - backtest
  - automation
  - SMC_ORB_VWAP_SCALP_A_PLUS
  - XAUUSD
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/30_SELECTED_ROUTINE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/50_BACKTEST_PROTOCOL.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01/20_DATA_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01/30_DETECTOR_RULES.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01

## 1_MASTER_TARGET

Automatiser le backtest comparatif de la routine `SMC_ORB_VWAP_SCALP_A_PLUS` sur XAUUSD M5/M15.
Produire : journal CSV, résultats par variant, verdict markdown — sans aucune exécution réelle.

## 3_INITIAL_NEED

Le child `GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01` prévoyait un bar replay manuel.
La vraie valeur est un runner automatisé : OHLCV → détection → scoring → simulation → rapport.

## 4_MASTER_PROJECT_PLAN

```text
OHLCV XAUUSD M5/M15
→ indicateurs (VWAP, ATR, sessions, ORB range)
→ détecteurs (sweep, BOS/CHOCH proxy, retest)
→ scorer /10
→ simulateur SL/TP (result_R, MFE, MAE)
→ export journal CSV
→ agrégation par variant
→ verdict markdown
```

## 5_GO_PLAN

1. Docs cadrage (ce GO).
2. Squelette `tools/strategy/daily_scalping/`.
3. Implémentation module par module : load → indicators → detectors → scorer → simulator → report.
4. Tests unitaires par module.
5. `run_backtest.py` orchestrateur.
6. Validation sur données synthétiques.
7. Verdict markdown auto-généré.

## 6_SCOPE_LIMITS

- Pas d'exécution d'ordre réel.
- Pas de connexion broker.
- Pas de live, pas de paper forward dans ce GO.
- Pas de modification des index globaux.
- Données OHLCV fournies en CSV — pas de fetch broker automatique dans ce GO.

## 7_PIPELINE_CIBLE

```bash
python tools/strategy/daily_scalping/run_backtest.py \
  --symbol XAUUSD \
  --timeframe M5 \
  --context-timeframe M15 \
  --input data/market/xauusd_m5.csv \
  --context-input data/market/xauusd_m15.csv \
  --out artifacts/backtests/daily_scalping

python tools/strategy/daily_scalping/report.py \
  --input artifacts/backtests/daily_scalping/xauusd_m5_journal.csv \
  --out-doc docs/chantiers/.../30_BACKTEST_VERDICT_01.md
```

## 8_VARIANTS

```text
ORB_ONLY
VWAP_PULLBACK_ONLY
SMC_SWEEP_ONLY
COMBINED_SMC_ORB_VWAP
```

## 13_ESTABLISHED

- SMC/ICT proxifié mécaniquement (swing high/low local, CHOCH/BOS proxy).
- Aucune subjectivité dans la détection — tout doit être reproductible.
- Backtest obligatoire avant toute promotion paper forward.

## 16_TODO

1. Implémenter `load_data.py` + `indicators.py`.
2. Implémenter `detectors.py` (ORB, sweep, BOS/CHOCH proxy, retest).
3. Implémenter `scorer.py` (/10).
4. Implémenter `simulator.py` (SL/TP, result_R, MFE, MAE).
5. Implémenter `report.py` (CSV + markdown).
6. Implémenter `run_backtest.py`.
7. Tests unitaires.
8. Validation données synthétiques → verdict markdown.
