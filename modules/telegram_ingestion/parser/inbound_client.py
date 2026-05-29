from collections.abc import Iterator
from typing import Protocol

from .message_schema import RawMessage


class InboundClient(Protocol):
    def get_messages(self, channel: str, limit: int = 100) -> list[RawMessage]: ...

    def iter_messages(self, channel: str) -> Iterator[RawMessage]: ...

    def add_event_handler(self, handler, event) -> None: ...


class MockClient:
    def __init__(self, messages: list[RawMessage] | None = None):
        self.messages = messages or []
        self.handlers: list[tuple] = []

    def get_messages(self, channel: str, limit: int = 100) -> list[RawMessage]:
        channel_msgs = [m for m in self.messages if m.channel == channel]
        return channel_msgs[:limit]

    def iter_messages(self, channel: str) -> Iterator[RawMessage]:
        channel_msgs = [m for m in self.messages if m.channel == channel]
        yield from channel_msgs

    def add_event_handler(self, handler, event) -> None:
        self.handlers.append((handler, event))
