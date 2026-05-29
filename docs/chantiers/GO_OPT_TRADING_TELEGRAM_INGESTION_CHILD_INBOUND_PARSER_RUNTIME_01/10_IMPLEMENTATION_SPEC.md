# 10_IMPLEMENTATION_SPEC

## Module structure

```text
modules/telegram_ingestion/
  __init__.py                    — exports: InboundClient, MessageReceiver, RawMessage
  parser/
    __init__.py
    inbound_client.py            — TelegramClient protocol + MockClient
    message_receiver.py          — MessageReceiver: reçoit/envoie messages via client
    message_schema.py            — RawMessage, InboundMessage dataclasses
```

## InboundClient protocol

```python
class InboundClient(Protocol):
    async def get_messages(self, channel: str, limit: int = 100) -> list[RawMessage]: ...
    async def iter_messages(self, channel: str) -> AsyncIterator[RawMessage]: ...
    async def add_event_handler(self, handler, event): ...
```

MockClient implémente le protocol avec une liste de messages pré-chargée.

## RawMessage schema

```python
@dataclass
class RawMessage:
    message_id: str
    channel: str
    sender: str | None
    timestamp: str  # ISO 8601
    raw_text: str
```

## MessageReceiver

- `receive_poll(client, channels, limit)` → list[RawMessage]
- `receive_stream(client, channels, handler)` → None (async event-driven)

Le receiver utilise l'abstraction client, pas Telethon directement.

## Tests

- `test_inbound_client_protocol` — MockClient implements protocol
- `test_inbound_client_get_messages` — returns expected messages
- `test_message_schema_creation` — RawMessage dataclass fields
- `test_message_receiver_poll` — poll returns messages
- `test_message_receiver_poll_empty` — poll returns [] for no messages
- `test_message_receiver_stream` — handler called for each message
- `test_no_network_in_tests` — no live API calls
- `test_no_secrets_in_repo` — no tokens/chat_ids
