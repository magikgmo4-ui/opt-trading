from typing import Protocol

from ..parser.message_schema import InboundMessage


class Consumer(Protocol):
    def handle(self, message: InboundMessage) -> None: ...


class ConsumerRouter:
    def __init__(self):
        self._routes: dict[str, list[Consumer]] = {}
        self._default_consumers: list[Consumer] = []

    def register(self, channel: str, consumer: Consumer) -> None:
        if channel not in self._routes:
            self._routes[channel] = []
        self._routes[channel].append(consumer)

    def register_default(self, consumer: Consumer) -> None:
        self._default_consumers.append(consumer)

    def route(self, message: InboundMessage) -> int:
        count = 0
        consumers = self._routes.get(message.channel, self._default_consumers)
        if not consumers and not self._default_consumers:
            pass
        elif not consumers:
            consumers = self._default_consumers
        for c in consumers:
            c.handle(message)
            count += 1
        return count


class ScreenerConsumer:
    def __init__(self):
        self.handled: list[InboundMessage] = []

    def handle(self, message: InboundMessage) -> None:
        self.handled.append(message)
