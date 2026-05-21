---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
depends_on:
  - GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_DATA_METHOD_REWORK_01
  - GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
  - GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01
status: open
lifecycle_stage: implementation
topic_keys:
  - opt-trading
  - strategy
  - daily_scalping
  - canonical_ohlcv
  - mt5_export
  - dukascopy
  - xauusd_180j
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/10_SOURCE_CHOICE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/20_MT5_EXPORT_RUNBOOK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/30_DUKASCOPY_IMPORT_RUNBOOK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/40_NORMALIZATION_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/50_ACCEPTANCE_REPORT.md
  - docs/index/inbox/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01.md
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01 — INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Obtenir et normaliser un dataset XAUUSD M5/M15 minimum 180 jours avec bid/ask/spread depuis MT5 ou Dukascopy, le normaliser vers `XAUUSD_M5_CANONICAL` / `XAUUSD_M15_CANONICAL`, et produire le premier verdict backtest stratégique valide sur `SMC_ORB_VWAP_SCALP_A_PLUS`.

## 2_CONTEXTE — Historique des blocages

| PR | Statut | Raison du blocage |
|---|---|---|
| #658 | smoke tech | GC=F Yahoo, 60j, CHOCH same-bar, min_score hors spec |
| #659 | mergée | chantier méthode rework, source canonique documentée |
| #662 | mergée | audit collectors : aucun PRIMARY_READY |
| #665 | mergée | Bitget XAUUSDT max 30j, CONTEXT_RECENT_ONLY |

**Conclusion de l'audit complet :** aucun collector du repo ne peut fournir 180j de M5 XAUUSD. MT5 ou Dukascopy est la seule voie vers un verdict valide.

## 3_OBJECTIF

Livrer :

1. `tools/strategy/daily_scalping/normalize_mt5.py` — normalisation CSV MT5 export vers contrat canonique
2. `tools/strategy/daily_scalping/normalize_dukascopy.py` — resample Dukascopy tick → M5/M15 canonique
3. `data/market/xauusd_m5_canonical.csv` + `data/market/xauusd_m15_canonical.csv` (à placer par l'opérateur)
4. Verdict backtest sur données canoniques réelles

## 4_CRITÈRES VERDICT VALIDE

```
source ∈ [mt5_export, dukascopy]
fenêtre ≥ 180 jours
SMC_SWEEP_ONLY ≥ 100 trades
COMBINED ≥ 100 trades (après rework CHOCH multi-bar)
régimes ≥ 3 (trend / range / high-vol)
→ PROMOTE / REWORK / REJECT autorisé
```

Tant que ces critères ne sont pas remplis → verdict = `NEED_DATA_UPGRADE`, pas de décision stratégique.

## 5_INVARIANTS

- Aucun ordre réel, aucun broker live execution
- Source GC=F/Bitget = smoke/context seulement
- Aucun index global
- Documenter clairement la période couverte, le broker source, et les sessions utilisées

## 6_PROCHAINE_ETAPE

Lire `10_SOURCE_CHOICE.md` — choisir entre MT5 et Dukascopy selon l'accès disponible.
