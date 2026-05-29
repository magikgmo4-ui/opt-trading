from collections.abc import Callable

from .inbound_client import InboundClient
from .message_schema import RawMessage


class MessageReceiver:
    def __init__(self, client: InboundClient):
        self._client = client

    def poll(
        self, channels: list[str], limit: int = 100
    ) -> list[RawMessage]:
        all_messages: list[RawMessage] = []
        for channel in channels:
            msgs = self._client.get_messages(channel, limit=limit)
            all_messages.extend(msgs)
        return all_messages

    def stream(
        self,
        channels: list[str],
        handler: Callable[[RawMessage], None],
    ) -> None:
        for channel in channels:
            for msg in self._client.iter_messages(channel):
                handler(msg)
