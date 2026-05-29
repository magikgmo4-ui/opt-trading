from modules.telegram_screener.parser import (
    parse_trade_setup,
    parse_news_alert,
    parse_alpha_signal,
    ScreenerSignal,
    SignalType,
)
from modules.telegram_screener.signal import (
    produce_screener_signal,
    produce_batch,
    adapt_to_telegram_claim,
    adapt_batch,
    ScreenerProducedSignal,
)


# ---------------------------------------------------------------------------
# Signal Producer
# ---------------------------------------------------------------------------

class TestSignalProducer:
    def test_produce_from_trade_setup(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000 SL 64000 TP 66000", source_channel="ch_signals")
        assert parsed is not None
        result = produce_screener_signal(parsed)
        assert isinstance(result, ScreenerProducedSignal)
        assert result.source == "telegram_screener"
        assert result.signal_type == "trade"
        assert result.channel == "ch_signals"
        assert result.pair == "BTCUSDT"
        assert result.direction == "LONG"
        assert result.entry_price == 65000.0
        assert result.sl == 64000.0
        assert result.tp == 66000.0
        assert result.confidence == "HIGH"
        assert result.raw_text == "BTCUSDT: LONG @ 65000 SL 64000 TP 66000"
        assert "BTCUSDT LONG @ 65000" in result.summary

    def test_produce_from_news(self):
        parsed = parse_news_alert("[MACRO] FOMC rate decision", source_channel="ch_news")
        assert parsed is not None
        result = produce_screener_signal(parsed)
        assert result.signal_type == "news"
        assert result.category == "MACRO"
        assert result.pair is None
        assert result.entry_price is None
        assert "[MACRO]" in result.summary

    def test_produce_from_alpha(self):
        parsed = parse_alpha_signal("AAPL: breakout pattern detected", source_channel="ch_alpha")
        assert parsed is not None
        result = produce_screener_signal(parsed)
        assert result.signal_type == "alpha"
        assert result.pair == "AAPL"
        assert "breakout" in result.summary

    def test_produce_sets_produced_at(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000")
        assert parsed is not None
        result = produce_screener_signal(parsed)
        assert result.produced_at is not None
        assert "T" in result.produced_at

    def test_produce_generates_uuid(self):
        parsed = parse_trade_setup("ETHUSDT: SHORT @ 3500")
        assert parsed is not None
        result = produce_screener_signal(parsed)
        assert len(result.id) == 36
        assert result.id.count("-") == 4

    def test_custom_source(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000")
        assert parsed is not None
        result = produce_screener_signal(parsed, source="my_custom_source")
        assert result.source == "my_custom_source"

    def test_produce_batch_empty(self):
        assert produce_batch([]) == []

    def test_produce_batch_multiple(self):
        t = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        n = parse_news_alert("[MACRO] Test", source_channel="ch")
        assert t is not None and n is not None
        results = produce_batch([t, n])
        assert len(results) == 2
        assert results[0].signal_type == "trade"
        assert results[1].signal_type == "news"

    def test_to_dict_output(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        assert parsed is not None
        result = produce_screener_signal(parsed)
        d = result.to_dict()
        assert d["source"] == "telegram_screener"
        assert d["signal_type"] == "trade"
        assert d["payload"]["pair"] == "BTCUSDT"
        assert d["payload"]["direction"] == "LONG"
        assert d["payload"]["entry_price"] == 65000.0

    def test_produce_trade_no_sl_tp_low_confidence(self):
        parsed = parse_trade_setup("SOLUSDT: LONG @ 145", source_channel="ch")
        assert parsed is not None
        result = produce_screener_signal(parsed)
        assert result.confidence == "LOW"
        assert result.sl is None
        assert result.tp is None


# ---------------------------------------------------------------------------
# Desk Pro Adapter
# ---------------------------------------------------------------------------

class TestDeskProAdapter:
    def test_adapt_trade_to_telegram_claim(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000 SL 64000 TP 66000", source_channel="ch")
        assert parsed is not None
        signal = produce_screener_signal(parsed)
        claim = adapt_to_telegram_claim(signal, channel_id="test_channel")

        assert claim["input_class"] == "telegram_claim.v1"
        assert claim["source"] == "telegram_screener"
        assert claim["channel_id"] == "test_channel"
        assert claim["symbol"] == "BTCUSDT"
        assert claim["claim_type"] == "trade_context"
        assert claim["text"] == "BTCUSDT: LONG @ 65000 SL 64000 TP 66000"
        assert claim["entities"]["direction"] == "long"
        assert 65000.0 in claim["entities"]["levels"]
        assert 64000.0 in claim["entities"]["levels"]
        assert 66000.0 in claim["entities"]["levels"]
        assert claim["entities"]["confidence"] == 0.85

    def test_adapt_news_to_telegram_claim(self):
        parsed = parse_news_alert("[MACRO] FOMC decision", source_channel="ch")
        assert parsed is not None
        signal = produce_screener_signal(parsed)
        claim = adapt_to_telegram_claim(signal)

        assert claim["input_class"] == "telegram_claim.v1"
        assert claim["claim_type"] == "news_alert"
        assert claim["symbol"] == ""
        assert claim["entities"]["levels"] == []

    def test_adapt_alpha_to_telegram_claim(self):
        parsed = parse_alpha_signal("AAPL: breakout", source_channel="ch")
        assert parsed is not None
        signal = produce_screener_signal(parsed)
        claim = adapt_to_telegram_claim(signal)

        assert claim["claim_type"] == "alpha_signal"
        assert claim["symbol"] == "AAPL"
        assert claim["entities"]["confidence"] == 0.35

    def test_adapt_batch(self):
        t = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        n = parse_news_alert("[MACRO] Test", source_channel="ch")
        assert t is not None and n is not None
        signals = produce_batch([t, n])
        claims = adapt_batch(signals, channel_id="batch_ch")
        assert len(claims) == 2
        assert claims[0]["claim_type"] == "trade_context"
        assert claims[1]["claim_type"] == "news_alert"

    def test_claim_id_format(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        assert parsed is not None
        signal = produce_screener_signal(parsed)
        claim = adapt_to_telegram_claim(signal)
        assert claim["claim_id"].startswith("tg_claim_")
        assert "BTCUSDT" in claim["claim_id"]

    def test_confidence_mapping(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="ch")
        assert parsed is not None
        signal = produce_screener_signal(parsed)
        claim = adapt_to_telegram_claim(signal)
        assert claim["entities"]["confidence"] == 0.35  # LOW

    def test_refs_format(self):
        parsed = parse_trade_setup("BTCUSDT: LONG @ 65000", source_channel="my_channel")
        assert parsed is not None
        signal = produce_screener_signal(parsed)
        claim = adapt_to_telegram_claim(signal, channel_id="my_ch", message_id="msg_001")
        assert "telegram://my_ch/msg_001" in claim["refs"]["telegram_message_ref"]
