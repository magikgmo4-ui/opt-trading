---
doc_id: GO_SPACEX_TV_ALERT_AUTOMATION_ENGINE_01_INITIAL
doc_type: initial_project_doc
go_id: GO_SPACEX_TV_ALERT_AUTOMATION_ENGINE_01
parent_go: GO_SPACEX_TV_AUTOMATION_MAX_01
status: draft
created_at: 2026-06-12
---

# GO_SPACEX_TV_ALERT_AUTOMATION_ENGINE_01

## Objective

Automated TradingView alert lifecycle based on SPCX enriched data:
- SMC structures → alert placement at key levels
- Webhook fires → analytics (count, direction, win rate)
- Adaptive: modify/delete alerts as market regime changes

## Components

| File | Role |
|------|------|
| `alert_engine/engine.py` | Decision engine + analytics + TV dispatch |
| `alert_engine/__init__.py` | Public API |

## Alert Types (auto-managed)

| Alert | Trigger | Auto? |
|-------|---------|-------|
| SPCX_HEARTBEAT_1M | Always active | ✅ permanent |
| SPCX_VWAP_RECLAIM | Price within 0.5% of VWAP | ✅ dynamic |
| SPCX_ORB_BREAK_UP | Break above ORB high | ✅ dynamic |
| SPCX_FVG_BULLISH_ZONE | Bullish FVG detected | ✅ dynamic |
| SPCX_FVG_BEARISH_ZONE | Bearish FVG detected | ✅ dynamic |
| SPCX_BOS_LEVEL | BOS confirmed | ✅ dynamic |
| SPCX_VOLUME_SPIKE | Volume > 2x average | ✅ dynamic |

## Analytics tracked

- `fire_count`: total fires per alert
- `fire_directions`: UP/DOWN/NEUTRAL per fire
- `last_fired_at`: timestamp
- `price_level`: trigger price

## Usage

```python
from modules.spcx_v2.alert_engine import AlertAutomationEngine

engine = AlertAutomationEngine()

# Evaluate enriched data → decisions
decisions = engine.evaluate(enriched_data)

# Dispatch (dry-run first)
results = engine.dispatch(decisions, dry_run=True)

# Record webhook fires
engine.record_fire(webhook_event)

# Get analytics
analytics = engine.get_analytics()
```
