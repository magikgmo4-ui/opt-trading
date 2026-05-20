---
doc_id: GO_TELEGRAM_LATENCY_BACKTEST_01_BACKTEST_OUTPUT_SCHEMA
doc_type: schema
repo: opt-trading
go_id: GO_TELEGRAM_LATENCY_BACKTEST_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_BACKTEST_OUTPUT_SCHEMA

## Output JSON (latency_backtest.py)

Structure:

```json
{
  "path": "C:\\\\...\\\\telegram_send.jsonl",
  "since": "",
  "until": "",
  "summary": {
    "count": 0,
    "ok_count": 0,
    "ok_rate": 0.0,
    "latency_ms_all": {
      "count": 0
    },
    "latency_ms_ok": {
      "count": 0
    },
    "by_source": {
      "notification_dispatcher:signal_received": {
        "count": 12,
        "ok_count": 12,
        "ok_rate": 1.0,
        "latency_ms": {
          "count": 12,
          "min_ms": 110,
          "p50_ms": 220,
          "p90_ms": 410,
          "p95_ms": 510,
          "p99_ms": 610,
          "max_ms": 650
        }
      }
    }
  }
}
```

## Invariants

- pas de chat_id/token dans l’output
- `source` est un label libre (caller) et peut être agrégé
