import pytest

from modules.telegram_ingestion import (
    RawMessage,
    InboundMessage,
    detect_type,
    extract_metadata,
    normalize_message,
)


class TestTypeDetector:
    def test_detect_text(self):
        assert detect_type("hello world", "user") == "text"

    def test_detect_link(self):
        assert detect_type("check https://t.me/abc", "user") == "link"

    def test_detect_link_no_sender(self):
        assert detect_type("visit http://example.com") == "link"

    def test_detect_poll_by_sender(self):
        assert detect_type("vote now", "poll_bot") == "poll"

    def test_detect_poll_by_content(self):
        assert detect_type("Poll: what do you think?", "user") == "poll"

    def test_detect_image_by_sender(self):
        assert detect_type("", "media_bot") == "image"

    def test_detect_image_precedence_over_link(self):
        assert detect_type("https://example.com/img.jpg", "media_bot") == "image"

    def test_detect_empty_text(self):
        assert detect_type("") == "text"

    def test_detect_empty_text_with_sender(self):
        assert detect_type("", "user") == "text"

    def test_detect_none_sender(self):
        assert detect_type("hello", None) == "text"


class TestMetadataExtractor:
    def test_extract_mentions(self):
        result = extract_metadata("hello @user1 and @user2")
        assert result["mentions"] == ["@user1", "@user2"]

    def test_extract_hashtags(self):
        result = extract_metadata("check #btc and #eth")
        assert result["hashtags"] == ["#btc", "#eth"]

    def test_extract_links(self):
        result = extract_metadata("visit https://t.me/abc and http://example.com")
        assert result["links"] == ["https://t.me/abc", "http://example.com"]

    def test_extract_all(self):
        result = extract_metadata("@user check #btc https://t.me/abc")
        assert result["mentions"] == ["@user"]
        assert result["hashtags"] == ["#btc"]
        assert result["links"] == ["https://t.me/abc"]

    def test_extract_no_metadata(self):
        result = extract_metadata("plain text")
        assert result["mentions"] == []
        assert result["hashtags"] == []
        assert result["links"] == []

    def test_extract_empty_text(self):
        result = extract_metadata("")
        assert result["mentions"] == []
        assert result["hashtags"] == []
        assert result["links"] == []

    def test_extract_none_text(self):
        result = extract_metadata(None)
        assert result["mentions"] == []
        assert result["hashtags"] == []
        assert result["links"] == []


class TestMessageNormalizer:
    def test_normalize_text(self):
        raw = RawMessage(message_id="1", channel="ch", raw_text="hello", sender="user")
        inbound = normalize_message(raw)
        assert isinstance(inbound, InboundMessage)
        assert inbound.message_id == "1"
        assert inbound.channel == "ch"
        assert inbound.raw_text == "hello"
        assert inbound.normalized_type == "text"
        assert inbound.metadata is not None

    def test_normalize_link(self):
        raw = RawMessage(message_id="2", channel="ch", raw_text="check https://t.me/abc")
        inbound = normalize_message(raw)
        assert inbound.normalized_type == "link"
        assert "https://t.me/abc" in inbound.metadata["links"]

    def test_normalize_poll(self):
        raw = RawMessage(message_id="3", channel="ch", raw_text="Poll: what do you think?", sender="poll_bot")
        inbound = normalize_message(raw)
        assert inbound.normalized_type == "poll"

    def test_normalize_with_metadata(self):
        raw = RawMessage(message_id="4", channel="ch", raw_text="@user check #btc https://t.me/abc")
        inbound = normalize_message(raw)
        assert inbound.metadata["mentions"] == ["@user"]
        assert inbound.metadata["hashtags"] == ["#btc"]
        assert inbound.metadata["links"] == ["https://t.me/abc"]

    def test_normalize_minimal(self):
        raw = RawMessage(message_id="5", channel="ch", raw_text="hi")
        inbound = normalize_message(raw)
        assert inbound.sender is None
        assert inbound.metadata == {"mentions": [], "hashtags": [], "links": []}
