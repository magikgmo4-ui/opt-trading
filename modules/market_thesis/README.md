# Market Thesis Engine

Unified market thesis engine for opt-trading.

Transforms collected data into structured, actionable market theses
consumable by DeskPro, Voice Operator, LocalCMS, and API JSON.

## Status

**PR2 — Context Aggregator / Source Readers**

- [x] `models.py` — Pydantic v2 models (PR1)
- [x] `schemas/market_thesis_v1.json` — JSON Schema Draft 2020-12 (PR1)
- [x] `config.py` — Source paths, symbol normalization, alias maps
- [x] `source_status.py` — Freshness evaluation (fresh/warm/stale/expired/missing/error)
- [x] `source_readers.py` — 10 source readers (JSONL + JSON)
- [x] `context_aggregator.py` — Aggregates all sources into `MarketContextInput`
- [x] Unit tests (149 tests: models + schema + readers + aggregator + status)

## Sources Supported

| Source | Contract | Format |
|--------|----------|--------|
| Webhook Events | `webhook_event.v1` | `state/events.jsonl` |
| CDP Events | `signal_event.v1` | `state/events_cdp.jsonl` |
| Market Metrics | `market_metrics.v1` | `data/data_center/views/market_metrics/by_symbol/{SYM}.json` |
| Multi-TF Analysis | `multitf_analysis_input.v1` | `data/data_center/views/multitf_analysis_input.v1/by_symbol/{SYM}.json` |
| Multi-TF Scores | `multitf_setup_score.v1` | `data/data_center/views/multitf_setup_score.v1/by_symbol/{SYM}.json` |
| Signal Events DC | `signal_event.v1` | `data/data_center/views/signal_event.v1/by_symbol/{SYM}/latest.json` |
| Vision Coinglass | `vision_context.coinglass.v1` | `data/deskpro/inputs/vision_context/coinglass/latest.json` |
| Vision Analysis | `vision_analysis.v1` | `data/data_center/views/vision_analysis/by_symbol/{SYM}.json` |
| Telegram Signals | `telegram_signal.v1` | `data/telegram_screener/signals/*.json` |
| Telegram Signals DC | `telegram_signals.v1` | `data/data_center/views/telegram_signals/by_symbol/{SYM}/latest.json` |

## Usage (PR2)

```python
from modules.market_thesis.context_aggregator import aggregate

# Aggregate all available sources for BTC
ctx = aggregate("BTC")

print(f"Symbol: {ctx.symbol}")
print(f"Freshness: {ctx.freshness_summary}")
print(f"Events: {len(ctx.raw_events)}")
print(f"Setups: {len(ctx.priority_inputs)}")
print(f"Missing sources: {ctx.missing_sources}")
print(f"Has data: {ctx.has_any_data}")

# Context is ready for thesis_engine (PR3-PR5)
```

## Event Alias Normalization

| Raw | Canonical |
|-----|-----------|
| `orb_break_high` | `ORB_HIGH_BREAK` |
| `orb_break_low` | `ORB_LOW_BREAK` |
| `volume_spike` | `VOLUME_SURGE` |
| `vwap_reclaim` | `VWAP_RECLAIM` |
| `vwap_loss` | `VWAP_LOSS` |
| `bos` | `BOS` |
| `choch` | `CHOCH` |

## Freshness Levels

| State | Age |
|-------|-----|
| `fresh` | <= 5 min |
| `warm` | <= 30 min |
| `stale` | <= 4 hours |
| `expired` | > 4 hours |
| `missing` | source absent |
| `error` | source illisible |

## Constraints

- Read-only — no trade execution
- No broker integration
- No DeskPro/Voice/LocalCMS integration yet
- No runtime pipeline — data ingestion only
- Additive architecture — no existing contracts modified
- Never crashes on missing/invalid sources

## Tests

```bash
pytest tests/market_thesis -q       # 149 tests
bash modules/market_thesis/scripts/sanity_check.sh
```

## Requirements

- Python 3.11+
- pydantic >= 2.0
- jsonschema >= 4.0
