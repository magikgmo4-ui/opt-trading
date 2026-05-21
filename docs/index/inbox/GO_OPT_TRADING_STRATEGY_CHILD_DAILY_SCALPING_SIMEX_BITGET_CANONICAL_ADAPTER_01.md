---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01_INBOX
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01
parent_go_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
depends_on: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
status: open
surface: index_inbox
source_kind: canonical
updated_at: 2026-05-20
topic_keys:
  - daily_scalping
  - simex_bitget_bridge
  - canonical_adapter
  - fetch_bitget
  - xauusdt_ohlcv
  - context_recent_only
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01/10_IMPLEMENTATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01/20_ACCEPTANCE_REPORT.md
  - tools/strategy/daily_scalping/fetch_bitget.py
---

# GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01

**État:** Open — livrable produit, acceptance PASS
**Branche:** `go/GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_SIMEX_BITGET_CANONICAL_ADAPTER_01`
**Parent:** `GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01`

Fetcher XAUUSDT M5/M15 via Bitget API, production CSV canonique avec spread réel.

## Finding critique

**Bitget max ~30j M5 historique** (testé 2026-05-20). Classification révisée :
`simex_bitget_bridge` : `PRIMARY_WITH_GAPS → CONTEXT_RECENT_ONLY`

## Livrable

`tools/strategy/daily_scalping/fetch_bitget.py`

```bash
python tools/strategy/daily_scalping/fetch_bitget.py --out data/market --days 30
```

Produit :
- `data/market/xauusdt_m5_bitget.csv` — 8 599 barres 30j, spread=0.01 USD
- `data/market/xauusdt_m15_bitget.csv` — 2 867 barres 30j

## Backtest smoke 30j (min_score=4)

| Variant | Trades | Exp R | Verdict |
|---|---:|---:|---|
| ORB_ONLY | 214 | -0.14 | REJECT |
| VWAP_PULLBACK_ONLY | 25 | +0.41 | NEED_MORE_DATA |
| SMC_SWEEP_ONLY | 1 | -1.0 | NEED_MORE_DATA |
| COMBINED | 0 | — | NO_DATA |

VWAP_PULLBACK signal positif à surveiller sur fenêtre plus longue.

## Bloquant persistant

MT5/Dukascopy export toujours obligatoire pour verdict 180j valide.
