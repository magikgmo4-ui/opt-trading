import pytest

from modules.telegram_ingestion import InboundMessage
from modules.telegram_ingestion.distribution import Consumer, ConsumerRouter, ScreenerConsumer


class TestConsumerProtocol:
    def test_screener_consumer_implements_protocol(self):
        c = ScreenerConsumer()
        assert hasattr(c, "handle")


class TestConsumerRouter:
    def test_register_and_route(self):
        router = ConsumerRouter()
        collected = []

        class TestConsumer:
            def handle(self, msg): collected.append(msg)

        consumer = TestConsumer()
        msg = InboundMessage(message_id="1", channel="ch", sender=None, timestamp="t", raw_text="hello")
        router.register("ch", consumer)
        count = router.route(msg)
        assert count == 1
        assert len(collected) == 1
        assert collected[0].message_id == "1"

    def test_channel_routing(self):
        router = ConsumerRouter()
        ch1_msgs = []
        ch2_msgs = []

        class Ch1Consumer:
            def handle(self, msg): ch1_msgs.append(msg)

        class Ch2Consumer:
            def handle(self, msg): ch2_msgs.append(msg)

        router.register("ch1", Ch1Consumer())
        router.register("ch2", Ch2Consumer())

        msg1 = InboundMessage(message_id="1", channel="ch1", sender=None, timestamp="t", raw_text="a")
        msg2 = InboundMessage(message_id="2", channel="ch2", sender=None, timestamp="t", raw_text="b")

        router.route(msg1)
        router.route(msg2)

        assert len(ch1_msgs) == 1
        assert len(ch2_msgs) == 1

    def test_default_consumer(self):
        router = ConsumerRouter()
        collected = []

        class DefaultConsumer:
            def handle(self, msg): collected.append(msg)

        router.register_default(DefaultConsumer())
        msg = InboundMessage(message_id="1", channel="unknown", sender=None, timestamp="t", raw_text="x")
        count = router.route(msg)
        assert count == 1
        assert len(collected) == 1

    def test_multiple_consumers_per_channel(self):
        router = ConsumerRouter()
        c1_msgs = []
        c2_msgs = []

        class C1:
            def handle(self, msg): c1_msgs.append(msg)

        class C2:
            def handle(self, msg): c2_msgs.append(msg)

        router.register("ch", C1())
        router.register("ch", C2())

        msg = InboundMessage(message_id="1", channel="ch", sender=None, timestamp="t", raw_text="x")
        count = router.route(msg)
        assert count == 2
        assert len(c1_msgs) == 1
        assert len(c2_msgs) == 1

    def test_no_registration(self):
        router = ConsumerRouter()
        msg = InboundMessage(message_id="1", channel="ch", sender=None, timestamp="t", raw_text="x")
        count = router.route(msg)
        assert count == 0

    def test_route_returns_count(self):
        router = ConsumerRouter()
        collected = []

        class TC:
            def handle(self, msg): collected.append(msg)

        router.register("ch", TC())
        router.register("ch", TC())
        router.register("ch", TC())

        msg = InboundMessage(message_id="1", channel="ch", sender=None, timestamp="t", raw_text="x")
        count = router.route(msg)
        assert count == 3

    def test_default_and_channel_no_duplicate(self):
        router = ConsumerRouter()
        collected = []

        class TC:
            def handle(self, msg): collected.append(msg)

        tc = TC()
        router.register("ch", tc)
        router.register_default(TC())

        msg = InboundMessage(message_id="1", channel="ch", sender=None, timestamp="t", raw_text="x")
        count = router.route(msg)
        assert count == 1
        assert len(collected) == 1


class TestScreenerConsumer:
    def test_collects_messages(self):
        consumer = ScreenerConsumer()
        msg = InboundMessage(message_id="1", channel="ch", sender=None, timestamp="t", raw_text="hello")
        consumer.handle(msg)
        assert len(consumer.handled) == 1
        assert consumer.handled[0].message_id == "1"

    def test_collects_multiple(self):
        consumer = ScreenerConsumer()
        consumer.handle(InboundMessage(message_id="1", channel="ch", sender=None, timestamp="t", raw_text="a"))
        consumer.handle(InboundMessage(message_id="2", channel="ch", sender=None, timestamp="t", raw_text="b"))
        assert len(consumer.handled) == 2
