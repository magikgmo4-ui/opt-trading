---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
lifecycle_stage: research
topic_keys:
  - opt-trading
  - strategy
  - daily_scalping
  - data_method
  - canonical_ohlcv
  - derivatives_collector
  - bot_vision
  - visual_context
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/10_PR658_METHOD_AUDIT.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/20_DATA_SOURCE_HIERARCHY.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/30_CANONICAL_OHLCV_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/40_COLLECTOR_INTEGRATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/50_BOT_VISION_VALIDATION_LAYER.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01/60_REVISED_BACKTEST_PROTOCOL.md
  - docs/index/inbox/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Remplacer la source de données Yahoo Finance / GC=F (proxy fragile) par une méthode canonique prod collector / broker export, intégrer les données dérivatives existantes (OI, funding, liquidations, L/S ratio) comme couche de confirmation contextuelle, et définir le rôle de bot vision / visual_context comme couche de validation structurelle — le tout pour produire un verdict backtest robuste et reproductible sur `SMC_ORB_VWAP_SCALP_A_PLUS`.

## 2_CONTEXTE

### Pourquoi ce GO existe

Le GO précédent (`GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_BACKTEST_AUTOMATION_01`, PR #657) a livré le runner backtest complet. Le run initial sur données réelles (PR #658) a produit :

```
TECHNICAL_SMOKE_PASS       — runner fonctionne de bout en bout
STRATEGY_VERDICT_INVALID   — source données non conforme
DATA_METHOD_REWORK_REQUIRED
```

La PR #658 est reclassée en smoke technique. Le verdict stratégique ne peut pas être prononcé sur cette base.

### Problèmes de méthode identifiés

| Point | Problème |
|---|---|
| Source | GC=F Yahoo = proxy futures, pas flux XAUUSD broker réel |
| Données | Pas de bid/ask, spread réel, slippage broker |
| Fenêtre | 60 jours seulement (limite yfinance intraday), période atypique |
| SMC/COMBINED | 0 setup détecté — CHOCH proxy trop strict pour M5 |
| Score filter | min_score=4 utilisé pour contourner le filtre 7/10 hors spec |
| Verdict | Exploitable seulement pour dire : règles/data à revoir |

## 3_OBJECTIF

Produire :

1. **Un contrat OHLCV canonique** avec bid/ask/spread, source broker/prod collector, timezone normalisée UTC, sessions broker identifiées
2. **Un plan d'intégration derivatives** via `derivatives_collector` existant — OI, funding, liquidations, L/S ratio comme couche contextuelle
3. **Un protocole de validation visuelle** via bot vision / visual_context — confirmation CHOCH/BOS/FVG/OB sur screenshot
4. **Un protocole backtest révisé** : données canoniques → détection reworkée (CHOCH multi-bar) → simulation avec spread réel → verdict reproductible

## 4_INVARIANTS

- Ne pas connecter broker pour exécution d'ordre
- Aucune exécution réelle
- TradingView = alertes/observation uniquement, pas source OHLCV canonique
- Yahoo/GC=F = fallback smoke uniquement, jamais source primaire de verdict
- `visual_context` = couche evidence, pas source OHLCV
- Aucun index global

## 5_LIVRABLES

| Doc | Contenu |
|---|---|
| `10_PR658_METHOD_AUDIT.md` | Audit détaillé des défauts méthode PR #658 |
| `20_DATA_SOURCE_HIERARCHY.md` | Hiérarchie des sources : primaire → fallback |
| `30_CANONICAL_OHLCV_CONTRACT.md` | Schéma CSV/JSON canonique avec bid/ask/spread |
| `40_COLLECTOR_INTEGRATION_PLAN.md` | Plan branchement derivatives_collector |
| `50_BOT_VISION_VALIDATION_LAYER.md` | Protocole visual_context comme couche evidence |
| `60_REVISED_BACKTEST_PROTOCOL.md` | Protocole backtest end-to-end avec données canoniques |

## 6_PROCHAINE_ETAPE

Commencer par `10_PR658_METHOD_AUDIT.md` — figer le diagnostic avant tout rework de code.
