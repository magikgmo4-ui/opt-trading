---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
depends_on: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
status: open
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - strategy
  - daily_scalping
  - simex_bitget_bridge
  - canonical_adapter
  - xauusdt_ohlcv
  - fetch_bitget
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01/10_IMPLEMENTATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01/20_ACCEPTANCE_REPORT.md
  - docs/index/inbox/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Créer `tools/strategy/daily_scalping/fetch_bitget.py` — un fetcher standalone XAUUSDT M5/M15 via l'API Bitget, produisant un CSV canonique avec spread réel (ticker API), meilleure qualité que GC=F pour la fenêtre disponible.

## 2_FINDING_CRITIQUE — Profondeur historique Bitget M5

**Testé le 2026-05-20 :**

| Profondeur testée | XAUUSDT M5 disponible |
|---|---|
| 30 jours | ✅ ~8 640 bougies |
| 45 jours | ❌ 0 bougies |
| 60+ jours | ❌ 0 bougies |

**Conclusion : Bitget API limite à ~30 jours de M5 historique.**

Cela invalide l'hypothèse de 180 jours via simex_bitget_bridge. La classification est révisée :

```
simex_bitget_bridge : PRIMARY_WITH_GAPS → CONTEXT_RECENT_ONLY (max 30j M5)
```

Pour le verdict backtest 180 jours, **MT5/Dukascopy reste obligatoire**.

## 3_OBJECTIF RÉVISÉ

Ce chantier livre :

1. `fetch_bitget.py` — fetcher XAUUSDT M5/M15 Bitget avec pagination (dans la limite ~30j)
2. Spread réel via Bitget ticker API (bid/ask instantané, appliqué uniformément aux bougies historiques)
3. CSV canonique `data/market/xauusdt_m5_bitget.csv` + `xauusdt_m15_bitget.csv`
4. Source marquée `bitget_xauusdt_futures_approx` — clairement distinguée de `mt5_export`/`dukascopy`
5. Acceptance report avec métadonnées du run

Ce que ce chantier **ne livre pas** :
- Données historiques 180 jours via Bitget (impossible)
- Source PRIMARY_READY stricte (reste PRIMARY_READY_APPROX sur 30j)
- Modification du simex_bitget_bridge existant

## 4_VALEUR

Même sur 30 jours, XAUUSDT Bitget est supérieur à GC=F Yahoo pour :
- Instrument plus proche (futures or USDT vs futures or USD)
- Spread réel disponible via ticker (0.01 USD vs hardcodé 3.0 pips)
- Source explicitement marquée dans chaque ligne CSV
- Pas de limite yfinance 60j (30j Bitget, moins mais plus propre)

## 5_INVARIANTS

- Aucun ordre réel
- Ne pas modifier simex_bitget_bridge main logic
- Documenter clairement XAUUSDT ≠ XAUUSD spot dans source field
- Ne pas prétendre que 30j de Bitget = verdict 180j valide

## 6_PROCHAINE_ETAPE

Lire `10_IMPLEMENTATION_PLAN.md`.
