# 10_INBOUND_SPEC

## Ingestion pipeline

```text
Telegram API Client
  -> Message Receiver (polling/webhook)
    -> Raw Message Store
      -> Message Normalizer
        -> Consumer Router
          -> PF_TELEGRAM_SCREENER
          -> PF_DESK_PRO
          -> PF_DATA_CENTER
```

## Message format

```json
{
  "message_id": "string",
  "channel": "string",
  "sender": "string | null",
  "timestamp": "ISO8601",
  "raw_text": "string",
  "normalized": {
    "type": "text|image|poll|link",
    "content": "string",
    "mentions": ["string"],
    "hashtags": ["string"],
    "links": ["string"]
  }
}
```

## Module structure

```text
modules/telegram_ingestion/
  parser/
    __init__.py
    telegram_client.py
    message_receiver.py
    message_normalizer.py
    consumer_router.py
  tests/
    test_telegram_client.py
    test_message_receiver.py
    test_message_normalizer.py
    test_consumer_router.py
```
