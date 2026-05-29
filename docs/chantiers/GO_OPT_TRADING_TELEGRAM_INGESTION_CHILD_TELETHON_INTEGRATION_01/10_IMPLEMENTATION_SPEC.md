# 10_IMPLEMENTATION_SPEC

## Module changes

- `requirements.txt` : +telethon==1.43.2
- `modules/telegram_ingestion/parser/telethon_client.py` : nouveau
- `modules/telegram_ingestion/__init__.py` : export TelethonInboundClient

## TelethonInboundClient

```python
class TelethonInboundClient:
    def __init__(self, session: str, api_id: int, api_hash: str): ...
    def start(self) -> None: ...
    def get_messages(self, channel: str, limit: int = 100) -> list[RawMessage]: ...
    def iter_messages(self, channel: str) -> Iterator[RawMessage]: ...
    def add_event_handler(self, handler, event) -> None: ...
```

### Détails

- Lazy import de telethon dans `_ensure_client()` pour permettre le graceful degradation
- `start()` appelle `client.start()` (authentification)
- `get_messages()` utilise `client.get_messages(channel, limit=limit)` et mappe Message → RawMessage
- `iter_messages()` utilise `client.iter_messages(channel)` et yield RawMessage
- Mapping de Message Telethon vers RawMessage : `id → str(m.id)`, `sender.username → sender`, `date → .isoformat()`, `text → raw_text`

## Test pattern

- `@patch('modules.telegram_ingestion.parser.telethon_client.TelegramClient')` mock au niveau module
- Mock retourne des messages Telethon simulés
- 0 appel réseau, 0 secret
