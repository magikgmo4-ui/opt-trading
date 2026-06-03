import json
from pathlib import Path

from modules.telegram_screener.normalizer import (
    candidate_to_screener_signal,
    coinglass_dict_to_candidate,
    normalize_coinglass_dict,
    screener_signal_to_candidate,
)
from modules.telegram_screener.parser import (
    ScreenerSignal,
    SignalType,
    Direction,
    Confidence,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "telegram_screener"


def _load_fixture(name: str) -> list[dict]:
    path = FIXTURES / name
    return json.loads(path.read_text(encoding="utf-8"))


class TestCoinglassDictToCandidate:
    def test_valid_coinglass_dict(self):
        samples = _load_fixture("coinglass_alert_samples.json")
        whale_samples = [s for s in samples if "Hyperliquid巨鲸" in s["raw_text"]]
        assert len(whale_samples) > 0
        for sample in whale_samples:
            exp = sample["expected"]
            raw_dict = {**exp, "source_channel": sample["source_channel"]}
            cand = coinglass_dict_to_candidate(raw_dict)
            assert cand.source_channel == "coinglass_alerts"
            assert cand.asset == exp["asset"]
            assert cand.symbol == exp["symbol"]
            assert cand.direction == exp["direction"]
            assert cand.entry_min == exp["entry"]
            assert cand.entry_max == exp["entry"]
            assert cand.leverage == exp["leverage"]
            assert cand.parse_status == exp["parse_status"]
            assert cand.parse_confidence == exp["confidence"]
            assert cand.message_ref == exp["raw_text_ref"]
            assert cand.tp == []
            assert cand.sl is None

    def test_tp_list_non_empty_when_present(self):
        raw = {
            "tp1": 67000.0,
            "tp2": 68000.0,
            "tp3": None,
            "entry": 66000.0,
        }
        cand = coinglass_dict_to_candidate(raw)
        assert cand.tp == [67000.0, 68000.0]

    def test_minimal_dict_defaults(self):
        cand = coinglass_dict_to_candidate({})
        assert cand.source_channel == ""
        assert cand.asset is None
        assert cand.parse_status == "PARTIAL"
        assert cand.parse_confidence == "LOW"
        assert cand.tp == []
        assert cand.parse_errors == []

    def test_parse_errors_preserved(self):
        raw = {"parse_errors": ["no_sl_found", "no_tp_found"]}
        cand = coinglass_dict_to_candidate(raw)
        assert cand.parse_errors == ["no_sl_found", "no_tp_found"]


class TestScreenerSignalToCandidate:
    def test_trade_signal(self):
        signal = ScreenerSignal(
            source_channel="ch",
            signal_type=SignalType.TRADE,
            timestamp="2026-06-03T12:00:00Z",
            parsed_at="2026-06-03T12:00:01Z",
            raw_text="BTCUSDT: LONG @ 65000 SL 64000 TP 66000",
            pair="BTCUSDT",
            direction=Direction.LONG,
            price=65000.0,
            sl=64000.0,
            tp=66000.0,
            confidence=Confidence.HIGH,
        )
        cand = screener_signal_to_candidate(signal)
        assert cand.raw_message == signal.raw_text
        assert cand.source_channel == "ch"
        assert cand.symbol == "BTCUSDT"
        assert cand.direction == "LONG"
        assert cand.entry_min == 65000.0
        assert cand.entry_max == 65000.0
        assert cand.sl == 64000.0
        assert cand.tp == [66000.0]
        assert cand.parse_confidence == "HIGH"

    def test_news_signal(self):
        signal = ScreenerSignal(
            source_channel="ch",
            signal_type=SignalType.NEWS,
            timestamp="2026-06-03T12:00:00Z",
            parsed_at="2026-06-03T12:00:01Z",
            raw_text="[MACRO] FOMC decision",
            category="MACRO",
            confidence=Confidence.MEDIUM,
        )
        cand = screener_signal_to_candidate(signal)
        assert cand.direction is None
        assert cand.entry_min is None
        assert cand.symbol is None
        assert cand.tp == []

    def test_alpha_signal(self):
        signal = ScreenerSignal(
            source_channel="ch",
            signal_type=SignalType.ALPHA,
            timestamp="2026-06-03T12:00:00Z",
            parsed_at="2026-06-03T12:00:01Z",
            raw_text="AAPL: breakout pattern",
            pair="AAPL",
            confidence=Confidence.LOW,
        )
        cand = screener_signal_to_candidate(signal)
        assert cand.symbol == "AAPL"
        assert cand.direction is None
        assert cand.tp == []

    def test_metadata_leverage_preserved(self):
        signal = ScreenerSignal(
            source_channel="ch",
            signal_type=SignalType.TRADE,
            timestamp="2026-06-03T12:00:00Z",
            parsed_at="2026-06-03T12:00:01Z",
            raw_text="BTCUSDT: LONG @ 65000",
            pair="BTCUSDT",
            direction=Direction.LONG,
            price=65000.0,
            metadata={"leverage": 25},
        )
        cand = screener_signal_to_candidate(signal)
        assert cand.leverage == 25

    def test_no_tp_when_sl_only(self):
        signal = ScreenerSignal(
            source_channel="ch",
            signal_type=SignalType.TRADE,
            timestamp="2026-06-03T12:00:00Z",
            parsed_at="2026-06-03T12:00:01Z",
            raw_text="BTCUSDT: LONG @ 65000 SL 64000",
            pair="BTCUSDT",
            direction=Direction.LONG,
            price=65000.0,
            sl=64000.0,
            confidence=Confidence.MEDIUM,
        )
        cand = screener_signal_to_candidate(signal)
        assert cand.tp == []
        assert cand.sl == 64000.0
        assert cand.parse_confidence == "MEDIUM"


class TestCandidateToScreenerSignal:
    def test_full_candidate(self):
        from modules.telegram_screener.schema import SignalCandidate

        cand = SignalCandidate(
            raw_message="BTCUSDT: LONG @ 65000 SL 64000 TP 66000",
            source_channel="ch",
            asset="BTC",
            symbol="BTCUSDT",
            direction="LONG",
            entry_min=65000.0,
            entry_max=65000.0,
            tp=[66000.0],
            sl=64000.0,
            leverage=25,
            timeframe="1h",
            parse_status="PARSED",
            parse_confidence="HIGH",
            parse_errors=[],
            message_ref="ch:123",
            created_at="2026-06-03T12:00:00Z",
        )
        signal = candidate_to_screener_signal(cand, signal_type=SignalType.TRADE)
        assert signal.source_channel == "ch"
        assert signal.signal_type == SignalType.TRADE
        assert signal.pair == "BTCUSDT"
        assert signal.direction == Direction.LONG
        assert signal.price == 65000.0
        assert signal.sl == 64000.0
        assert signal.tp == 66000.0
        assert signal.confidence == Confidence.HIGH
        assert signal.metadata["leverage"] == 25
        assert signal.metadata["timeframe"] == "1h"
        assert signal.metadata["parse_status"] == "PARSED"
        assert signal.metadata["message_ref"] == "ch:123"

    def test_partial_candidate_no_direction(self):
        from modules.telegram_screener.schema import SignalCandidate

        cand = SignalCandidate(
            raw_message="BTC: some alpha signal",
            source_channel="ch",
            asset="BTC",
            symbol="BTC",
            parse_status="PARTIAL",
            parse_confidence="LOW",
        )
        signal = candidate_to_screener_signal(cand, signal_type=SignalType.ALPHA)
        assert signal.signal_type == SignalType.ALPHA
        assert signal.pair == "BTC"
        assert signal.direction is None
        assert signal.price is None
        assert signal.confidence == Confidence.LOW

    def test_unknown_direction_becomes_none(self):
        from modules.telegram_screener.schema import SignalCandidate

        cand = SignalCandidate(
            raw_message="test",
            source_channel="ch",
            direction="INVALID",
        )
        signal = candidate_to_screener_signal(cand)
        assert signal.direction is None

    def test_multiple_tp_first_used(self):
        from modules.telegram_screener.schema import SignalCandidate

        cand = SignalCandidate(
            raw_message="test",
            source_channel="ch",
            symbol="BTCUSDT",
            direction="LONG",
            tp=[66000.0, 67000.0, 68000.0],
        )
        signal = candidate_to_screener_signal(cand)
        assert signal.tp == 66000.0


class TestNormalizeCoinglassDict:
    def test_integration(self):
        samples = _load_fixture("coinglass_alert_samples.json")
        whale_samples = [s for s in samples if "Hyperliquid巨鲸" in s["raw_text"]]
        assert len(whale_samples) > 0
        for sample in whale_samples:
            exp = sample["expected"]
            raw_dict = {**exp, "source_channel": sample["source_channel"]}
            signal = normalize_coinglass_dict(raw_dict)
            assert signal.source_channel == "coinglass_alerts"
            assert signal.pair == exp["symbol"]
            assert signal.direction == Direction(exp["direction"])
            assert signal.price == exp["entry"]
            assert signal.metadata["leverage"] == exp["leverage"]
            assert signal.metadata["parse_status"] == exp["parse_status"]
            assert signal.sl is None
            assert signal.tp is None

    def test_empty_dict_graceful(self):
        signal = normalize_coinglass_dict({})
        assert signal.source_channel == ""
        assert signal.pair is None
        assert signal.direction is None


class TestRoundtrip:
    def test_screener_signal_roundtrip(self):
        original = ScreenerSignal(
            source_channel="ch",
            signal_type=SignalType.TRADE,
            timestamp="2026-06-03T12:00:00Z",
            parsed_at="2026-06-03T12:00:01Z",
            raw_text="BTCUSDT: LONG @ 65000 SL 64000 TP 66000",
            pair="BTCUSDT",
            direction=Direction.LONG,
            price=65000.0,
            sl=64000.0,
            tp=66000.0,
            size="2.5",
            confidence=Confidence.HIGH,
        )
        cand = screener_signal_to_candidate(original)
        restored = candidate_to_screener_signal(cand, signal_type=SignalType.TRADE)
        assert restored.source_channel == original.source_channel
        assert restored.pair == original.pair
        assert restored.direction == original.direction
        assert restored.price == original.price
        assert restored.sl == original.sl
        assert restored.tp == original.tp
        assert restored.confidence == original.confidence
        assert restored.raw_text == original.raw_text


class TestToDict:
    def test_signal_candidate_to_dict(self):
        from modules.telegram_screener.schema import SignalCandidate

        cand = SignalCandidate(
            raw_message="test",
            source_channel="ch",
            asset="BTC",
            symbol="BTCUSDT",
            direction="LONG",
            entry_min=65000.0,
            entry_max=65500.0,
            tp=[66000.0, 67000.0],
            sl=64000.0,
            leverage=25,
            timeframe="1h",
            parse_status="PARSED",
            parse_confidence="HIGH",
            parse_errors=[],
            message_ref="ch:1",
            created_at="2026-06-03T12:00:00Z",
        )
        d = cand.to_dict()
        assert d["raw_message"] == "test"
        assert d["source_channel"] == "ch"
        assert d["asset"] == "BTC"
        assert d["symbol"] == "BTCUSDT"
        assert d["direction"] == "LONG"
        assert d["entry_min"] == 65000.0
        assert d["entry_max"] == 65500.0
        assert d["tp"] == [66000.0, 67000.0]
        assert d["sl"] == 64000.0
        assert d["leverage"] == 25
        assert d["timeframe"] == "1h"
        assert d["parse_status"] == "PARSED"
        assert d["parse_confidence"] == "HIGH"
        assert d["parse_errors"] == []
        assert d["message_ref"] == "ch:1"
        assert d["created_at"] == "2026-06-03T12:00:00Z"
