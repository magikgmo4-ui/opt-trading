from collections.abc import Iterator
from datetime import timezone

from .message_schema import RawMessage
from .inbound_client import InboundClient


class TelethonInboundClient:
    def __init__(self, session: str, api_id: int, api_hash: str):
        self._session = session
        self._api_id = api_id
        self._api_hash = api_hash
        self._client = None
        self._started = False

    def _ensure_client(self):
        if self._client is not None:
            return
        try:
            from telethon import TelegramClient as _TelethonClient
            import telethon.sync  # noqa: F401
        except ImportError:
            raise ImportError(
                "telethon is required. Install with: pip install telethon"
            )
        self._client = _TelethonClient(self._session, self._api_id, self._api_hash)

    def start(self) -> None:
        self._ensure_client()
        if not self._started:
            self._client.start()
            self._started = True

    def get_messages(self, channel: str, limit: int = 100) -> list[RawMessage]:
        self._ensure_client()
        messages = self._client.get_messages(channel, limit=limit)
        return [self._to_raw(msg, channel) for msg in messages]

    def iter_messages(self, channel: str) -> Iterator[RawMessage]:
        self._ensure_client()
        for msg in self._client.iter_messages(channel):
            yield self._to_raw(msg, channel)

    def add_event_handler(self, handler, event) -> None:
        self._ensure_client()
        self._client.add_event_handler(handler, event)

    @staticmethod
    def _to_raw(msg, channel: str) -> RawMessage:
        return RawMessage(
            message_id=str(msg.id),
            channel=channel,
            sender=msg.sender.username if msg.sender else None,
            timestamp=msg.date.replace(tzinfo=timezone.utc).isoformat() if msg.date else None,
            raw_text=msg.text or "",
        )
