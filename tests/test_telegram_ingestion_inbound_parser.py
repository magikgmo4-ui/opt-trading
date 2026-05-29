import pytest

from modules.telegram_ingestion import InboundClient, MockClient, MessageReceiver, RawMessage, InboundMessage


class TestRawMessage:
    def test_creation_with_all_fields(self):
        msg = RawMessage(
            message_id="1",
            channel="test_channel",
            raw_text="hello",
            sender="user1",
            timestamp="2026-01-01T00:00:00",
        )
        assert msg.message_id == "1"
        assert msg.channel == "test_channel"
        assert msg.raw_text == "hello"
        assert msg.sender == "user1"
        assert msg.timestamp == "2026-01-01T00:00:00"

    def test_creation_minimal_fields(self):
        msg = RawMessage(message_id="2", channel="ch", raw_text="hi")
        assert msg.message_id == "2"
        assert msg.channel == "ch"
        assert msg.raw_text == "hi"
        assert msg.sender is None
        assert msg.timestamp is not None

    def test_default_timestamp_is_iso8601(self):
        msg = RawMessage(message_id="3", channel="ch", raw_text="t")
        assert "T" in msg.timestamp
        assert "+" in msg.timestamp


class TestInboundMessage:
    def test_creation(self):
        msg = InboundMessage(
            message_id="1",
            channel="ch",
            sender="u1",
            timestamp="2026-01-01T00:00:00",
            raw_text="hello",
        )
        assert msg.message_id == "1"
        assert msg.normalized_type == "text"

    def test_from_raw(self):
        raw = RawMessage(message_id="42", channel="alpha", raw_text="signal")
        inbound = InboundMessage.from_raw(raw, normalized_type="alpha")
        assert inbound.message_id == "42"
        assert inbound.channel == "alpha"
        assert inbound.raw_text == "signal"
        assert inbound.normalized_type == "alpha"
        assert inbound.sender is None

    def test_from_raw_with_sender(self):
        raw = RawMessage(message_id="7", channel="news", raw_text="news", sender="bot")
        inbound = InboundMessage.from_raw(raw, normalized_type="news")
        assert inbound.sender == "bot"


class TestInboundClientProtocol:
    def test_mock_client_has_required_methods(self):
        client = MockClient()
        assert hasattr(client, "get_messages")
        assert hasattr(client, "iter_messages")
        assert hasattr(client, "add_event_handler")


class TestMockClient:
    def test_get_messages_returns_preset_list(self):
        msgs = [
            RawMessage(message_id="1", channel="ch1", raw_text="a"),
            RawMessage(message_id="2", channel="ch1", raw_text="b"),
        ]
        client = MockClient(messages=msgs)
        result = client.get_messages("ch1")
        assert len(result) == 2
        assert result[0].message_id == "1"
        assert result[1].message_id == "2"

    def test_get_messages_respects_limit(self):
        msgs = [
            RawMessage(message_id=str(i), channel="ch", raw_text=str(i))
            for i in range(10)
        ]
        client = MockClient(messages=msgs)
        result = client.get_messages("ch", limit=3)
        assert len(result) == 3

    def test_get_messages_filters_by_channel(self):
        msgs = [
            RawMessage(message_id="1", channel="ch1", raw_text="a"),
            RawMessage(message_id="2", channel="ch2", raw_text="b"),
        ]
        client = MockClient(messages=msgs)
        result = client.get_messages("ch1")
        assert len(result) == 1
        assert result[0].channel == "ch1"

    def test_get_messages_empty(self):
        client = MockClient()
        result = client.get_messages("ch")
        assert result == []

    def test_iter_messages_yields_messages(self):
        msgs = [
            RawMessage(message_id="1", channel="ch", raw_text="a"),
            RawMessage(message_id="2", channel="ch", raw_text="b"),
        ]
        client = MockClient(messages=msgs)
        collected = list(client.iter_messages("ch"))
        assert len(collected) == 2

    def test_iter_messages_empty(self):
        client = MockClient()
        collected = list(client.iter_messages("ch"))
        assert collected == []

    def test_add_event_handler(self):
        client = MockClient()
        def handler(msg): pass
        client.add_event_handler(handler, "event")
        assert len(client.handlers) == 1
        assert client.handlers[0][0] is handler
        assert client.handlers[0][1] == "event"


class TestMessageReceiver:
    def test_poll_returns_messages(self):
        msgs = [
            RawMessage(message_id="1", channel="ch1", raw_text="a"),
            RawMessage(message_id="2", channel="ch1", raw_text="b"),
        ]
        client = MockClient(messages=msgs)
        receiver = MessageReceiver(client)
        result = receiver.poll(["ch1"])
        assert len(result) == 2

    def test_poll_respects_limit(self):
        msgs = [RawMessage(message_id=str(i), channel="ch", raw_text=str(i)) for i in range(10)]
        client = MockClient(messages=msgs)
        receiver = MessageReceiver(client)
        result = receiver.poll(["ch"], limit=3)
        assert len(result) == 3

    def test_poll_empty(self):
        client = MockClient()
        receiver = MessageReceiver(client)
        result = receiver.poll(["ch"])
        assert result == []

    def test_poll_multiple_channels(self):
        msgs = [
            RawMessage(message_id="1", channel="ch1", raw_text="a"),
            RawMessage(message_id="2", channel="ch2", raw_text="b"),
        ]
        client = MockClient(messages=msgs)
        receiver = MessageReceiver(client)
        result = receiver.poll(["ch1", "ch2"])
        assert len(result) == 2

    def test_stream_calls_handler_per_message(self):
        msgs = [
            RawMessage(message_id="1", channel="ch", raw_text="a"),
            RawMessage(message_id="2", channel="ch", raw_text="b"),
        ]
        client = MockClient(messages=msgs)
        receiver = MessageReceiver(client)
        handled = []

        def handler(msg):
            handled.append(msg)

        receiver.stream(["ch"], handler)
        assert len(handled) == 2
        assert handled[0].message_id == "1"
        assert handled[1].message_id == "2"

    def test_stream_empty(self):
        client = MockClient()
        receiver = MessageReceiver(client)
        handled = []

        def handler(msg):
            handled.append(msg)

        receiver.stream(["ch"], handler)
        assert handled == []
