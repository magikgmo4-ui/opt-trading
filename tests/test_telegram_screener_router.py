from datetime import datetime, timezone

from modules.telegram_screener.parser import ScreenerSignal, SignalType, Direction, Confidence
from modules.telegram_screener.registry import Channel, ChannelRegistry, TrustTier, load_channel_registry
from modules.telegram_screener.router import FilterRouter, RouteDecision
from pathlib import Path


def _signal(
    source_channel: str = "TG_SRC_SIGNALS_01",
    signal_type: SignalType = SignalType.TRADE,
    category: str | None = None,
) -> ScreenerSignal:
    now = datetime.now(timezone.utc).isoformat()
    return ScreenerSignal(
        source_channel=source_channel,
        signal_type=signal_type,
        timestamp=now,
        parsed_at=now,
        raw_text="BTCUSDT: LONG @ 65000",
        pair="BTCUSDT",
        direction=Direction.LONG,
        price=65000.0,
        category=category,
        confidence=Confidence.HIGH,
    )


def _registry(*channels: Channel) -> ChannelRegistry:
    return ChannelRegistry(version=1, updated_at="2026-05-28", channels=list(channels))


def _channel(
    alias: str = "TG_SRC_SIGNALS_01",
    trust_tier: TrustTier = TrustTier.C,
    categories: list[str] | None = None,
    expected_parsers: list[str] | None = None,
    enabled: bool = True,
) -> Channel:
    return Channel(
        alias=alias,
        kind="channel",
        title=alias,
        trust_tier=trust_tier,
        categories=categories or ["signals", "macro"],
        expected_parsers=expected_parsers or ["trade_claim", "setup"],
        enabled=enabled,
    )


class TestFilterRouter:
    def test_route_accepts_valid_signal(self):
        ch = _channel()
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal())
        assert result.accepted
        assert result.channel == ch
        assert result.rejection_reason is None

    def test_route_rejects_unknown_channel(self):
        reg = _registry()
        router = FilterRouter(reg)
        result = router.route(_signal(source_channel="UNKNOWN"))
        assert not result.accepted
        assert result.channel is None
        assert "unknown" in result.rejection_reason.lower()

    def test_route_rejects_disabled_channel(self):
        ch = _channel(enabled=False)
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal())
        assert not result.accepted
        assert result.channel == ch
        assert "disabled" in result.rejection_reason.lower()

    def test_route_rejects_below_min_tier(self):
        ch = _channel(trust_tier=TrustTier.D)
        reg = _registry(ch)
        router = FilterRouter(reg, min_tier=TrustTier.C)
        result = router.route(_signal())
        assert not result.accepted
        assert result.channel == ch
        assert "below" in result.rejection_reason.lower()

    def test_route_accepts_at_min_tier(self):
        ch = _channel(trust_tier=TrustTier.C)
        reg = _registry(ch)
        router = FilterRouter(reg, min_tier=TrustTier.C)
        result = router.route(_signal())
        assert result.accepted

    def test_route_accepts_above_min_tier(self):
        ch = _channel(trust_tier=TrustTier.A)
        reg = _registry(ch)
        router = FilterRouter(reg, min_tier=TrustTier.C)
        result = router.route(_signal())
        assert result.accepted

    def test_route_rejects_parser_mismatch(self):
        ch = _channel(expected_parsers=["news"])
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(signal_type=SignalType.TRADE))
        assert not result.accepted
        assert "parser" in result.rejection_reason.lower()

    def test_route_accepts_news_with_news_parser(self):
        ch = _channel(expected_parsers=["news"])
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(signal_type=SignalType.NEWS))
        assert result.accepted

    def test_route_accepts_alpha_with_alpha_parser(self):
        ch = _channel(expected_parsers=["alpha"])
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(signal_type=SignalType.ALPHA))
        assert result.accepted

    def test_route_accepts_trade_with_setup_parser(self):
        ch = _channel(expected_parsers=["setup"])
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(signal_type=SignalType.TRADE))
        assert result.accepted

    def test_route_category_mismatch_logged_not_rejected(self):
        ch = _channel(categories=["news", "macro"])
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(category="signals"))
        assert result.accepted
        assert "category_mismatch" in result.metadata

    def test_route_no_category_mismatch_when_signal_has_no_category(self):
        ch = _channel(categories=["signals", "macro"])
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(category=None))
        assert result.accepted
        assert "category_mismatch" not in result.metadata

    def test_route_category_match_accepted(self):
        ch = _channel(categories=["signals", "macro"])
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(category="signals"))
        assert result.accepted
        assert "category_mismatch" not in result.metadata

    def test_route_batch_mixed(self):
        ch = _channel()
        reg = _registry(ch)
        router = FilterRouter(reg)
        signals = [
            _signal(source_channel="TG_SRC_SIGNALS_01"),
            _signal(source_channel="UNKNOWN"),
            _signal(source_channel="TG_SRC_SIGNALS_01"),
        ]
        results = router.route_batch(signals)
        assert len(results) == 3
        assert results[0].accepted
        assert not results[1].accepted
        assert results[2].accepted

    def test_default_min_tier_is_D(self):
        reg = _registry()
        router = FilterRouter(reg)
        assert router.min_tier == TrustTier.D

    def test_registry_property(self):
        reg = _registry()
        router = FilterRouter(reg)
        assert router.registry is reg

    def test_route_rejects_when_no_channels_in_registry(self):
        reg = ChannelRegistry(version=1, updated_at="2026-05-28", channels=[])
        router = FilterRouter(reg)
        result = router.route(_signal())
        assert not result.accepted
        assert result.channel is None

    def test_multiple_channels_route_to_correct_one(self):
        ch_a = _channel(alias="TG_SRC_SIGNALS_01", enabled=True)
        ch_b = _channel(alias="TG_SRC_NEWS_01", enabled=False)
        reg = _registry(ch_a, ch_b)
        router = FilterRouter(reg)
        result = router.route(_signal(source_channel="TG_SRC_SIGNALS_01"))
        assert result.accepted
        assert result.channel == ch_a

    def test_case_sensitivity_of_channel_alias(self):
        ch = _channel(alias="TG_SRC_SIGNALS_01")
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal(source_channel="tg_src_signals_01"))
        assert not result.accepted
        assert result.channel is None

    def test_route_creates_route_decision_dataclass(self):
        ch = _channel()
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal())
        assert isinstance(result, RouteDecision)
        assert hasattr(result, "accepted")
        assert hasattr(result, "channel")
        assert hasattr(result, "rejection_reason")
        assert hasattr(result, "metadata")

    def test_route_batch_returns_empty_list_for_empty_input(self):
        reg = _registry()
        router = FilterRouter(reg)
        results = router.route_batch([])
        assert results == []

    def test_route_with_registry_loaded_from_yaml(self):
        reg = load_channel_registry()
        router = FilterRouter(reg)
        result = router.route(_signal(source_channel="TG_SRC_SIGNALS_01"))
        assert not result.accepted
        assert "disabled" in result.rejection_reason.lower()

        result = router.route(_signal(source_channel="TG_SRC_NEWS_01", signal_type=SignalType.NEWS))
        assert result.accepted

    def test_route_multiple_rejection_reasons_first_wins(self):
        ch = _channel(trust_tier=TrustTier.D, enabled=False)
        reg = _registry(ch)
        router = FilterRouter(reg)
        result = router.route(_signal())
        assert not result.accepted
        assert "disabled" in result.rejection_reason.lower()
