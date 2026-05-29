import pytest
from unittest.mock import MagicMock, patch

from modules.telegram_ingestion import RawMessage


class TestTelethonInboundClient:
    @pytest.fixture
    def mock_telegram_client(self):
        with patch("telethon.TelegramClient") as mock:
            mock_instance = MagicMock()
            mock.return_value = mock_instance
            yield mock, mock_instance

    def test_start_calls_telethon_start(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        client.start()
        mock_instance.start.assert_called_once()

    def test_get_messages_returns_raw_messages(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        fake_msg = MagicMock()
        fake_msg.id = 42
        fake_msg.sender.username = "testuser"
        fake_msg.date = None
        fake_msg.text = "hello"
        mock_instance.get_messages.return_value = [fake_msg]

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        result = client.get_messages("test_channel")

        assert len(result) == 1
        assert isinstance(result[0], RawMessage)
        assert result[0].message_id == "42"
        assert result[0].channel == "test_channel"
        assert result[0].sender == "testuser"
        assert result[0].raw_text == "hello"
        mock_instance.get_messages.assert_called_once_with("test_channel", limit=100)

    def test_get_messages_respects_limit(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        fake_msg = MagicMock()
        fake_msg.id = 1
        fake_msg.sender.username = "u"
        fake_msg.date = None
        fake_msg.text = "msg"
        mock_instance.get_messages.return_value = [fake_msg] * 5

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        result = client.get_messages("ch", limit=5)
        assert len(result) == 5
        mock_instance.get_messages.assert_called_once_with("ch", limit=5)

    def test_get_messages_empty(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        mock_instance.get_messages.return_value = []

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        result = client.get_messages("ch")
        assert result == []

    def test_iter_messages_yields_raw_messages(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        fake_msg = MagicMock()
        fake_msg.id = 7
        fake_msg.sender.username = "user"
        fake_msg.date = None
        fake_msg.text = "iter_msg"
        mock_instance.iter_messages.return_value = [fake_msg]

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        collected = list(client.iter_messages("ch"))
        assert len(collected) == 1
        assert collected[0].message_id == "7"

    def test_iter_messages_empty(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        mock_instance.iter_messages.return_value = []

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        collected = list(client.iter_messages("ch"))
        assert collected == []

    def test_add_event_handler(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        handler = MagicMock()

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        client.add_event_handler(handler, "event")
        mock_instance.add_event_handler.assert_called_once_with(handler, "event")

    def test_message_mapping_null_sender(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        fake_msg = MagicMock()
        fake_msg.id = 1
        fake_msg.sender = None
        fake_msg.date = None
        fake_msg.text = "text"
        mock_instance.get_messages.return_value = [fake_msg]

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        result = client.get_messages("ch")
        assert result[0].sender is None

    def test_start_called_once_on_multiple_calls(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        client.start()
        client.start()
        mock_instance.start.assert_called_once()

    def test_get_messages_handles_none_text(self, mock_telegram_client):
        mock, mock_instance = mock_telegram_client
        fake_msg = MagicMock()
        fake_msg.id = 1
        fake_msg.sender = MagicMock()
        fake_msg.sender.username = "u"
        fake_msg.date = None
        fake_msg.text = None
        mock_instance.get_messages.return_value = [fake_msg]

        from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient
        client = TelethonInboundClient("session", 12345, "hash")
        result = client.get_messages("ch")
        assert result[0].raw_text == ""
