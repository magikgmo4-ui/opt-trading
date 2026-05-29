# 10_IMPLEMENTATION_SPEC

## Module structure

```text
modules/telegram_ingestion/
  distribution/
    __init__.py
    consumer_router.py    — Consumer protocol + ConsumerRouter
```

## Consumer protocol

```python
class Consumer(Protocol):
    def handle(self, message: InboundMessage) -> None: ...
```

## ConsumerRouter

- `register(channel: str, consumer: Consumer) → None` — ajoute un consumer pour un canal
- `register_default(consumer: Consumer) → None` — consumer pour tous les canaux non listés
- `route(message: InboundMessage) → int` — dispatch le message, retourne le nombre de consumers appelés

## ScreenerConsumer (stub)

- Implémente Consumer
-  `handle(message)` → appelle ScreenerPipeline.run(message.raw_text, message.channel)
- Pour ce GO : défini mais peut être un stub simple qui collecte les messages (testable)

## Tests

- `test_consumer_protocol` — une classe stub implémente Consumer
- `test_router_register` — register + route appelle le consumer
- `test_router_multiple_channels` — différents canaux → différents consumers
- `test_router_default` — canal non enregistré → default consumer
- `test_router_multiple_consumers` — plusieurs consumers pour un canal
- `test_router_no_consumer` — aucun consumer → 0 dispatch
- `test_screener_consumer_stub` — ScreenerConsumer collecte les messages
