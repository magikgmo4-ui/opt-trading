# 10_EVENT_TRACKER_SPEC

## Event pipeline

```text
POST /tv (webhook)
  -> webhook_to_perf.py (normalize)
    -> perf_db (SQLite WAL)
      -> position_tracker.py (candidate -> active -> closed)
        -> metrics
```

## Event schema

```json
{
  "event_id": "string (uuid)",
  "type": "entry|exit|pnl",
  "timestamp": "ISO8601",
  "pair": "string",
  "direction": "LONG|SHORT",
  "size": "number",
  "price": "number",
  "pnl": "number | null",
  "status": "candidate|active|closed"
}
```

## Module structure

```text
modules/perf_engine/
  tracker/
    __init__.py
    event_schema.py
    event_tracker.py
    position_lifecycle.py
  tests/
    test_event_tracker.py
    test_position_lifecycle.py
```
