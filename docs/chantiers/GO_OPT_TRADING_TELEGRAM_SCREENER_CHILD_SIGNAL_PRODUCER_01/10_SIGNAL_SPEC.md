# 10_SIGNAL_SPEC

## Screener signal format

```json
{
  "id": "string (uuid)",
  "source": "telegram_screener",
  "signal_type": "trade|news|alpha",
  "channel": "string",
  "parsed_at": "ISO8601",
  "produced_at": "ISO8601",
  "payload": {
    "pair": "string | null",
    "direction": "LONG|SHORT|null",
    "entry_price": "number | null",
    "sl": "number | null",
    "tp": "number | null",
    "size": "string | null",
    "category": "string | null",
    "confidence": "HIGH|MEDIUM|LOW|null",
    "raw_text": "string",
    "summary": "string"
  }
}
```

## Desk Pro integration

Le signal est poussé via le mécanisme existant de Desk Pro (events/messages).
Un adapter `desk_pro_signal_adapter.py` normalise le signal pour la consommation Desk Pro.

## Structure module

```text
modules/telegram_screener/
  signal/
    __init__.py
    signal_schema.py
    signal_producer.py
    desk_pro_adapter.py
  tests/
    test_signal_producer.py
    test_desk_pro_adapter.py
```
