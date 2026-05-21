---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-20
topic_keys:
  - daily_scalping
  - canonical_ohlcv
  - mt5_export
  - dukascopy
  - xauusd_180j
  - normalize_mt5
  - normalize_dukascopy
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/10_SOURCE_CHOICE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/20_MT5_EXPORT_RUNBOOK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/30_DUKASCOPY_IMPORT_RUNBOOK.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/40_NORMALIZATION_CONTRACT.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01/50_ACCEPTANCE_REPORT.md
  - tools/strategy/daily_scalping/normalize_mt5.py
  - tools/strategy/daily_scalping/normalize_dukascopy.py
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01

**État:** Open — scripts livrés, en attente source opérateur
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`

Obtenir XAUUSD M5/M15 ≥ 180j via MT5 ou Dukascopy et produire le premier verdict backtest valide.

## Livrables code

| Script | Usage |
|---|---|
| `normalize_mt5.py` | Normalise export CSV MT5 History Center → canonique |
| `normalize_dukascopy.py` | Resample Dukascopy tick CSV → M5/M15 canonique |

## Action opérateur requise

```
Choisir : MT5 export (voir 20_MT5_EXPORT_RUNBOOK) ou Dukascopy (voir 30_DUKASCOPY_IMPORT_RUNBOOK)
Exporter XAUUSD M5/M15 minimum 2024-01-01 → 2025-12-31
Placer dans data/market/raw/
Exécuter normalize_mt5.py ou normalize_dukascopy.py
Valider + rejouer backtest
Remplir 50_ACCEPTANCE_REPORT
```

## Bloquant verdict

```
Verdict stratégique SMC_ORB_VWAP_SCALP_A_PLUS = BLOQUÉ
Raison : aucune source PRIMARY_READY disponible sans action opérateur
Débloqué par : fourniture dataset MT5 ou Dukascopy ≥ 180j
```

## Sources refusées

```
Yahoo/GC=F : SMOKE_ONLY
Bitget XAUUSDT : CONTEXT_RECENT_ONLY (max 30j)
```
