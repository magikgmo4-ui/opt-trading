from pathlib import Path

from modules.telegram_screener.parser import SignalType
from modules.telegram_screener.registry import Channel, ChannelRegistry, TrustTier, load_channel_registry
from modules.telegram_screener.pipeline import ScreenerPipeline, PipelineResult
from modules.telegram_screener.router import FilterRouter


TRADE_TEXT = "BTCUSDT: LONG @ 65000 SL 64000 TP 66000"
NEWS_TEXT = "[MACRO] FOMC rate decision"
ALPHA_TEXT = "AAPL: breakout pattern detected"
UNPARSEABLE_TEXT = "some random text"


def _registry_with_enabled(alias: str = "TG_SRC_SIGNALS_01") -> ChannelRegistry:
    return ChannelRegistry(
        version=1,
        updated_at="2026-05-28",
        channels=[
            Channel(
                alias=alias,
                kind="channel",
                title=alias,
                trust_tier=TrustTier.C,
                categories=["signals", "macro", "news"],
                expected_parsers=["trade_claim", "setup", "news", "alpha"],
                enabled=True,
            ),
        ],
    )


class TestScreenerPipeline:
    def test_pipeline_full_trade_to_claim(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        result = pipe.run(TRADE_TEXT, "TG_SRC_SIGNALS_01")
        assert result.succeeded
        assert result.signal is not None
        assert result.signal.signal_type == SignalType.TRADE
        assert result.route is not None
        assert result.route.accepted
        assert result.produced is not None
        assert result.produced.signal_type == "trade"
        assert result.claim is not None
        assert result.claim["input_class"] == "telegram_claim.v1"
        assert result.claim["claim_type"] == "trade_context"
        assert result.claim["symbol"] == "BTCUSDT"

    def test_pipeline_full_news_to_claim(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        result = pipe.run(NEWS_TEXT, "TG_SRC_SIGNALS_01")
        assert result.succeeded
        assert result.signal is not None
        assert result.signal.signal_type == SignalType.NEWS
        assert result.claim["claim_type"] == "news_alert"

    def test_pipeline_full_alpha_to_claim(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        result = pipe.run(ALPHA_TEXT, "TG_SRC_SIGNALS_01")
        assert result.succeeded
        assert result.signal is not None
        assert result.signal.signal_type == SignalType.ALPHA
        assert result.claim["claim_type"] == "alpha_signal"

    def test_pipeline_rejects_unparseable_text(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        result = pipe.run(UNPARSEABLE_TEXT, "TG_SRC_SIGNALS_01")
        assert not result.succeeded
        assert "unparseable" in result.error.lower()
        assert result.signal is None
        assert result.produced is None
        assert result.claim is None

    def test_pipeline_rejects_unknown_channel(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        result = pipe.run(TRADE_TEXT, "UNKNOWN_CHANNEL")
        assert not result.succeeded
        assert "rejected" in result.error.lower()
        assert result.route is not None
        assert not result.route.accepted

    def test_pipeline_rejects_disabled_channel(self):
        reg = ChannelRegistry(
            version=1,
            updated_at="2026-05-28",
            channels=[
                Channel(
                    alias="TG_SRC_DISABLED_01",
                    kind="channel",
                    title="Disabled",
                    trust_tier=TrustTier.C,
                    categories=["signals"],
                    expected_parsers=["trade_claim"],
                    enabled=False,
                ),
            ],
        )
        pipe = ScreenerPipeline(reg)
        result = pipe.run(TRADE_TEXT, "TG_SRC_DISABLED_01")
        assert not result.succeeded
        assert "disabled" in result.error.lower()

    def test_pipeline_rejects_below_min_tier(self):
        reg = ChannelRegistry(
            version=1,
            updated_at="2026-05-28",
            channels=[
                Channel(
                    alias="TG_SRC_LOW_TIER_01",
                    kind="channel",
                    title="Low Tier",
                    trust_tier=TrustTier.D,
                    categories=["signals"],
                    expected_parsers=["trade_claim"],
                    enabled=True,
                ),
            ],
        )
        pipe = ScreenerPipeline(reg, min_tier=TrustTier.C)
        result = pipe.run(TRADE_TEXT, "TG_SRC_LOW_TIER_01")
        assert not result.succeeded
        assert "below" in result.error.lower()

    def test_pipeline_rejects_parser_mismatch(self):
        reg = ChannelRegistry(
            version=1,
            updated_at="2026-05-28",
            channels=[
                Channel(
                    alias="TG_SRC_NEWS_ONLY_01",
                    kind="channel",
                    title="News Only",
                    trust_tier=TrustTier.A,
                    categories=["news"],
                    expected_parsers=["news"],
                    enabled=True,
                ),
            ],
        )
        pipe = ScreenerPipeline(reg)
        result = pipe.run(TRADE_TEXT, "TG_SRC_NEWS_ONLY_01")
        assert not result.succeeded
        assert "parser" in result.error.lower()

    def test_pipeline_accepts_with_min_tier_threshold(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg, min_tier=TrustTier.D)
        result = pipe.run(TRADE_TEXT, "TG_SRC_SIGNALS_01")
        assert result.succeeded

    def test_pipeline_succeeded_property_false_when_error(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        result = pipe.run(UNPARSEABLE_TEXT, "TG_SRC_SIGNALS_01")
        assert not result.succeeded

    def test_pipeline_succeeded_property_true_when_complete(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        result = pipe.run(TRADE_TEXT, "TG_SRC_SIGNALS_01")
        assert result.succeeded

    def test_pipeline_batch_mixed_results(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        inputs = [
            (TRADE_TEXT, "TG_SRC_SIGNALS_01"),
            (UNPARSEABLE_TEXT, "TG_SRC_SIGNALS_01"),
            (NEWS_TEXT, "TG_SRC_SIGNALS_01"),
        ]
        results = pipe.run_batch(inputs)
        assert len(results) == 3
        assert results[0].succeeded
        assert not results[1].succeeded
        assert results[2].succeeded

    def test_pipeline_batch_empty(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        results = pipe.run_batch([])
        assert results == []

    def test_pipeline_router_property(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        assert isinstance(pipe.router, FilterRouter)
        assert pipe.router.registry is reg

    def test_pipeline_preserves_channel_alias_in_claim(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        result = pipe.run(TRADE_TEXT, "TG_SRC_SIGNALS_01")
        assert result.claim["channel_id"] == "TG_SRC_SIGNALS_01"

    def test_pipeline_claim_has_required_fields(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        result = pipe.run(TRADE_TEXT, "TG_SRC_SIGNALS_01")
        claim = result.claim
        assert "input_class" in claim
        assert "claim_id" in claim
        assert "claim_ts" in claim
        assert "symbol" in claim
        assert "entities" in claim
        assert "refs" in claim

    def test_pipeline_default_registry_from_yaml(self):
        pipe = ScreenerPipeline()
        result = pipe.run(NEWS_TEXT, "TG_SRC_NEWS_01")
        assert result.succeeded

    def test_pipeline_rejected_result_no_produced_or_claim(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        result = pipe.run(UNPARSEABLE_TEXT, "TG_SRC_SIGNALS_01")
        assert result.produced is None
        assert result.claim is None

    def test_pipeline_error_message_clear_for_unparseable(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        result = pipe.run(UNPARSEABLE_TEXT, "TG_SRC_SIGNALS_01")
        assert "unparseable" in result.error

    def test_pipeline_error_message_clear_for_rejection(self):
        reg = _registry_with_enabled()
        pipe = ScreenerPipeline(reg)
        result = pipe.run(TRADE_TEXT, "UNKNOWN")
        assert "rejected" in result.error

    def test_pipeline_route_decision_available_even_when_rejected(self):
        pipe = ScreenerPipeline(_registry_with_enabled())
        result = pipe.run(TRADE_TEXT, "UNKNOWN")
        assert result.route is not None
        assert not result.route.accepted
