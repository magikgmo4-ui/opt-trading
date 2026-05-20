---
doc_id: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01_SIGNAL_SCHEMA
doc_type: signal_schema
repo: opt-trading
project: opt-trading
module: strategy
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_ROUTINE_01
chantier_parent: GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01
status: draft
lifecycle_stage: strategy_candidate
topic_keys: [opt-trading, strategy, daily_scalping, signal_schema, TradingView, Telegram, screener]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_PARENT_DAILY_SCALPING_RESEARCH_01/30_SELECTED_ROUTINE.md
---

# 40_SIGNAL_SCHEMA

## Objectif

Définir un schéma signal indépendant de la session, compatible avec TradingView, screener headless, Telegram, bot vision, DeskPro et journalisation.

## Signal minimal JSON

```json
{
  "strategy_id": "SMC_ORB_VWAP_SCALP_A_PLUS",
  "symbol": "XAUUSD",
  "market_type": "CFD_OR_SPOT_OR_PERP",
  "timeframe": "M5",
  "session": "NY_OPEN",
  "direction": "LONG_OR_SHORT",
  "bias_htf": "LONG_OR_SHORT_OR_NEUTRAL",
  "setup_type": "SWEEP_CHOCH_BOS_RETEST_OR_ORB_RETEST_OR_VWAP_PULLBACK",
  "orb_state": "NONE_OR_DEFINED_OR_BREAKOUT_OR_RETEST",
  "vwap_state": "ABOVE_OR_BELOW_OR_RECLAIM_OR_REJECT_OR_CHOP",
  "liquidity_state": "HIGH_SWEEP_OR_LOW_SWEEP_OR_INTERNAL_LIQUIDITY_OR_NONE",
  "structure_state": "NO_CHOCH_OR_CHOCH_OR_BOS_OR_CHOCH_BOS_DONE",
  "entry_state": "WATCH_OR_WAIT_RETEST_OR_ENTRY_VALID_OR_INVALIDATED",
  "entry_zone": {
    "min": 0.0,
    "max": 0.0
  },
  "stop_loss": 0.0,
  "tp1": 0.0,
  "tp2": 0.0,
  "risk_pct": 0.25,
  "rr_planned": 2.0,
  "setup_score": 0,
  "risk_status": "AUTHORIZED_OR_BLOCKED",
  "block_reason": "",
  "screenshot_before": "",
  "notes": ""
}
```

## Telegram format

```text
XAUUSD M5
STRATEGY: SMC_ORB_VWAP_SCALP_A_PLUS
SESSION: NY_OPEN
DIRECTION: SHORT
BIAS_HTF: SHORT
SETUP: HIGH_SWEEP_CHOCH_BOS_RETEST
VWAP: BELOW_OR_REJECT
ENTRY_ZONE: 2386.5-2388.0
SL: 2392.2
TP1: 2381.0
TP2: 2375.5
RR: 2.1
SCORE: 8/10
STATUS: WAIT_RETEST
RISK: AUTHORIZED
```

## États autorisés

### `setup_type`

```text
ORB_RETEST
VWAP_PULLBACK
SWEEP_CHOCH_BOS_RETEST
DONCHIAN_MOMENTUM_CRYPTO
MEAN_REVERSION_RANGE_ONLY
NEWS_SCALP_BLOCKED_BY_DEFAULT
```

### `risk_status`

```text
AUTHORIZED
BLOCKED_SCORE_LOW
BLOCKED_SPREAD
BLOCKED_NEWS
BLOCKED_RR_LOW
BLOCKED_DAILY_LOSS_LIMIT
BLOCKED_MAX_TRADES
BLOCKED_NO_RETEST
BLOCKED_NO_INVALIDATION
```

## Règle de publication

Un signal peut être envoyé à Telegram en `WATCH` ou `WAIT_RETEST`, mais ne peut être considéré `ENTRY_VALID` que si :

```text
setup_score >= 7
risk_status == AUTHORIZED
rr_planned >= 1.8
stop_loss is defined
entry_zone is defined
```

## 13_ESTABLISHED

Le schéma est une interface de documentation et de scoring. Il n'autorise pas l'exécution réelle.

## 16_TODO

- Créer un validateur JSON dédié après validation du protocole backtest.
- Ajouter un mapping exact vers le journal Google Sheets.
