import json
from pathlib import Path

from modules.telegram_ingestion.parser.message_schema import RawMessage
from modules.telegram_screener.parser import (
    parse_trade_setup,
    parse_news_alert,
    parse_alpha_signal,
    parse_coinglass_alert,
    normalize_signal,
    ScreenerSignal,
    SignalType,
    Direction,
)
from modules.telegram_screener.parser.signal_normalizer import classify_raw_text


FIXTURES = Path(__file__).resolve().parent / "fixtures" / "telegram_screener"


def _load_fixture(name: str) -> list[dict]:
    path = FIXTURES / name
    return json.loads(path.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Trade parser
# ---------------------------------------------------------------------------

class TestTradeParser:
    def test_valid_trade_setup_basic(self):
        result = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        assert result is not None
        assert result.signal_type == SignalType.TRADE
        assert result.pair == "BTCUSDT"
        assert result.direction == Direction.LONG
        assert result.price == 65000.0
        assert result.sl is None
        assert result.tp is None
        assert result.confidence.value == "LOW"

    def test_valid_trade_setup_with_sl_tp(self):
        result = parse_trade_setup("ETHUSDT: SHORT @ 3500 SL 3450 TP 3600", source_channel="ch")
        assert result is not None
        assert result.pair == "ETHUSDT"
        assert result.direction == Direction.SHORT
        assert result.price == 3500.0
        assert result.sl == 3450.0
        assert result.tp == 3600.0
        assert result.confidence.value == "HIGH"

    def test_valid_trade_setup_with_size(self):
        result = parse_trade_setup("SOLUSDT: LONG @ 145 SL 140 TP 155 SIZE 2.5", source_channel="ch")
        assert result is not None
        assert result.size == "2.5"
        assert result.confidence.value == "HIGH"

    def test_trade_setup_sl_only_medium_confidence(self):
        result = parse_trade_setup("DOGEUSDT: LONG @ 0.085 SL 0.080", source_channel="ch")
        assert result is not None
        assert result.price == 0.085
        assert result.sl == 0.080
        assert result.tp is None
        assert result.confidence.value == "MEDIUM"

    def test_invalid_format_returns_none(self):
        assert parse_trade_setup("just some random text") is None

    def test_empty_string_returns_none(self):
        assert parse_trade_setup("") is None

    def test_case_insensitive(self):
        result = parse_trade_setup("btcusdt: long @ 65000")
        assert result is not None
        assert result.pair == "BTCUSDT"
        assert result.direction == Direction.LONG

    def test_source_channel_propagated(self):
        result = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="my_channel")
        assert result is not None
        assert result.source_channel == "my_channel"

    def test_timestamp_propagated(self):
        result = parse_trade_setup("BTCUSDT: LONG @ 65000", timestamp="2026-05-28T12:00:00Z")
        assert result is not None
        assert result.timestamp == "2026-05-28T12:00:00Z"

    def test_large_price_with_commas(self):
        result = parse_trade_setup("BTCUSDT: LONG @ 68,500", source_channel="ch")
        assert result is not None
        assert result.price == 68500.0

    def test_to_dict_output(self):
        result = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        assert result is not None
        d = result.to_dict()
        assert d["signal_type"] == "trade"
        assert d["normalized"]["pair"] == "BTCUSDT"
        assert d["normalized"]["direction"] == "LONG"
        assert d["normalized"]["price"] == 65000.0
        assert d["normalized"]["confidence"] == "LOW"

    def test_fixture_samples_all_parse(self):
        samples = _load_fixture("trade_setup_samples.json")
        for s in samples:
            result = parse_trade_setup(s["raw"], source_channel=s["source_channel"])
            assert result is not None, f"Failed to parse: {s['raw']}"
            assert result.pair == s["pair"], f"pair mismatch for: {s['raw']}"
            assert result.direction.value == s["direction"], f"direction mismatch for: {s['raw']}"
            assert result.price == s["price"], f"price mismatch for: {s['raw']}"


# ---------------------------------------------------------------------------
# News parser
# ---------------------------------------------------------------------------

class TestNewsParser:
    def test_valid_news_alert(self):
        result = parse_news_alert("[MACRO] FOMC rate decision expected hawkish", source_channel="ch")
        assert result is not None
        assert result.signal_type == SignalType.NEWS
        assert result.category == "MACRO"
        assert result.confidence.value == "MEDIUM"

    def test_alert_category(self):
        result = parse_news_alert("[ALERT] Flash crash on BTC", source_channel="ch")
        assert result is not None
        assert result.category == "ALERT"

    def test_economic_category(self):
        result = parse_news_alert("[ECONOMIC] US CPI data release at 13:30 UTC", source_channel="ch")
        assert result is not None
        assert result.category == "ECONOMIC"

    def test_invalid_format_returns_none(self):
        assert parse_news_alert("no category brackets here") is None

    def test_empty_brackets_returns_none(self):
        result = parse_news_alert("[] just text")
        assert result is None

    def test_fixture_samples_all_parse(self):
        samples = _load_fixture("news_samples.json")
        for s in samples:
            result = parse_news_alert(s["raw"], source_channel=s["source_channel"])
            assert result is not None, f"Failed to parse: {s['raw']}"
            assert result.category == s["category"], f"category mismatch for: {s['raw']}"


# ---------------------------------------------------------------------------
# Alpha parser
# ---------------------------------------------------------------------------

class TestAlphaParser:
    def test_valid_alpha_signal(self):
        result = parse_alpha_signal("AAPL: breakout pattern detected on daily", source_channel="ch")
        assert result is not None
        assert result.signal_type == SignalType.ALPHA
        assert result.pair == "AAPL"
        assert result.confidence.value == "LOW"
        assert result.metadata.get("message") == "breakout pattern detected on daily"

    def test_crypto_ticker(self):
        result = parse_alpha_signal("BTC: dominance increasing above 60%", source_channel="ch")
        assert result is not None
        assert result.pair == "BTC"

    def test_eth_alpha(self):
        result = parse_alpha_signal("ETH: whale accumulation spotted at support", source_channel="ch")
        assert result is not None
        assert result.pair == "ETH"

    def test_invalid_format_returns_none(self):
        assert parse_alpha_signal("no colon separator") is None

    def test_ticker_too_long_returns_none(self):
        assert parse_alpha_signal("VERYLONGTICKER: message") is None

    def test_fixture_samples_all_parse(self):
        samples = _load_fixture("alpha_samples.json")
        for s in samples:
            result = parse_alpha_signal(s["raw"], source_channel=s["source_channel"])
            assert result is not None, f"Failed to parse: {s['raw']}"
            assert result.pair == s["ticker"], f"ticker mismatch for: {s['raw']}"


# ---------------------------------------------------------------------------
# Coinglass parser
# ---------------------------------------------------------------------------

class TestCoinglassParser:
    def test_valid_coinglass_alert_samples_parse(self):
        samples = _load_fixture("coinglass_alert_samples.json")
        for sample in samples:
            result = parse_coinglass_alert(
                RawMessage(
                    message_id=sample["message_id"],
                    channel=sample["source_channel"],
                    raw_text=sample["raw_text"],
                    timestamp=sample["timestamp"],
                )
            )
            assert result is not None
            expected = sample["expected"]
            assert result["asset"] == expected["asset"]
            assert result["parse_status"] == expected["parse_status"]
            assert result["confidence"] == expected["confidence"]
            assert result["raw_text_ref"] == f"{sample['source_channel']}:{sample['message_id']}"
            assert result["parse_errors"] == []
            if result["schema"] == "telegram_trade_signal_candidate.v1":
                assert result["symbol"] == expected["symbol"]
                assert result["direction"] == expected["direction"]
                assert result["entry"] == expected["entry"]
                assert result["leverage"] == expected["leverage"]
                assert result["exchange_source"] == expected["exchange_source"]
                assert result["notional_usd"] == expected["notional_usd"]
                assert result["message_timestamp"] == sample["timestamp"]
                assert result["tp1"] is None
                assert result["tp2"] is None
                assert result["tp3"] is None
                assert result["stop_loss"] is None
                assert result["timeframe"] is None
            else:
                assert result["transaction_type"] == expected["transaction_type"]
                assert result["amount_asset"] == expected["amount_asset"]
                assert result["amount_usd"] == expected["amount_usd"]
                assert result["from_entity"] == expected["from_entity"]
                assert result["to_entity"] == expected["to_entity"]
                assert result["from_identified"] == expected["from_identified"]
                assert result["to_identified"] == expected["to_identified"]

    def test_unknown_coinglass_format_returns_none(self):
        result = parse_coinglass_alert(
            RawMessage(
                message_id="1",
                channel="coinglass_alerts",
                raw_text="random coinglass text without a parsable whale setup",
                timestamp="2026-06-03T04:05:40+00:00",
            )
        )
        assert result is None

    def test_coinglass_transfer_format_parses(self):
        samples = _load_fixture("coinglass_alert_samples.json")
        transfer_samples = [s for s in samples if "大额转账" in s["raw_text"]]
        assert len(transfer_samples) > 0
        for sample in transfer_samples:
            result = parse_coinglass_alert(
                RawMessage(
                    message_id=sample["message_id"],
                    channel=sample["source_channel"],
                    raw_text=sample["raw_text"],
                    timestamp=sample["timestamp"],
                )
            )
            assert result is not None
            assert result["schema"] == "telegram_transfer_candidate.v1"
            expected = sample["expected"]
            assert result["asset"] == expected["asset"]
            assert result["amount_asset"] == expected["amount_asset"]
            assert result["amount_usd"] == expected["amount_usd"]
            assert result["from_entity"] == expected["from_entity"]
            assert result["to_entity"] == expected["to_entity"]
            assert result["from_identified"] == expected["from_identified"]
            assert result["to_identified"] == expected["to_identified"]
            assert result["transaction_type"] == expected["transaction_type"]
            assert result["confidence"] == expected["confidence"]
            assert result["parse_status"] == expected["parse_status"]
            assert result["parse_errors"] == []
            assert result["raw_text_ref"] == f"{sample['source_channel']}:{sample['message_id']}"

    def test_coinglass_whale_still_parses_after_transfer_addition(self):
        samples = _load_fixture("coinglass_alert_samples.json")
        whale_samples = [s for s in samples if "Hyperliquid巨鲸" in s["raw_text"]]
        assert len(whale_samples) > 0
        for sample in whale_samples:
            result = parse_coinglass_alert(
                RawMessage(
                    message_id=sample["message_id"],
                    channel=sample["source_channel"],
                    raw_text=sample["raw_text"],
                    timestamp=sample["timestamp"],
                )
            )
            assert result is not None
            assert result["schema"] == "telegram_trade_signal_candidate.v1"
            expected = sample["expected"]
            assert result["asset"] == expected["asset"]
            assert result["direction"] == expected["direction"]
            assert result["entry"] == expected["entry"]


# ---------------------------------------------------------------------------
# Signal normalizer
# ---------------------------------------------------------------------------

class TestSignalNormalizer:
    def test_normalize_trade_signal(self):
        signal = parse_trade_setup("BTCUSDT: LONG @ 65000 SL 64000 TP 66000", source_channel="ch")
        assert signal is not None
        d = normalize_signal(signal)
        assert d["signal_type"] == "trade"
        assert d["normalized"]["pair"] == "BTCUSDT"
        assert d["normalized"]["direction"] == "LONG"
        assert d["normalized"]["sl"] == 64000.0
        assert d["normalized"]["tp"] == 66000.0

    def test_normalize_news_signal(self):
        signal = parse_news_alert("[MACRO] FOMC decision", source_channel="ch")
        assert signal is not None
        d = normalize_signal(signal)
        assert d["signal_type"] == "news"
        assert d["normalized"]["category"] == "MACRO"

    def test_normalize_alpha_signal(self):
        signal = parse_alpha_signal("AAPL: breakout", source_channel="ch")
        assert signal is not None
        d = normalize_signal(signal)
        assert d["signal_type"] == "alpha"

    def test_normalized_dict_has_all_expected_keys(self):
        signal = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        assert signal is not None
        d = normalize_signal(signal)
        assert "source_channel" in d
        assert "signal_type" in d
        assert "timestamp" in d
        assert "parsed_at" in d
        assert "raw_text" in d
        assert "normalized" in d
        norm = d["normalized"]
        for key in ("pair", "direction", "price", "sl", "tp", "size", "category", "confidence"):
            assert key in norm, f"missing key: {key}"


# ---------------------------------------------------------------------------
# Classify raw text
# ---------------------------------------------------------------------------

class TestClassifyRawText:
    def test_classify_trade(self):
        assert classify_raw_text("BTCUSDT: LONG @ 65000") == "trade"

    def test_classify_news(self):
        assert classify_raw_text("[MACRO] FOMC decision") == "news"

    def test_classify_alpha(self):
        assert classify_raw_text("AAPL: breakout pattern") == "alpha"

    def test_classify_unknown(self):
        assert classify_raw_text("completely random text") is None
