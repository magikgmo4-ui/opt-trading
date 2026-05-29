from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..parser import ScreenerSignal, SignalType
from ..registry import Channel, ChannelRegistry, TrustTier


_SIGNAL_TYPE_TO_PARSER: dict[SignalType, list[str]] = {
    SignalType.TRADE: ["trade_claim", "setup"],
    SignalType.NEWS: ["news"],
    SignalType.ALPHA: ["alpha"],
}


@dataclass
class RouteDecision:
    signal: ScreenerSignal
    accepted: bool
    channel: Optional[Channel] = None
    rejection_reason: Optional[str] = None
    metadata: dict = field(default_factory=dict)


class FilterRouter:
    def __init__(
        self,
        registry: ChannelRegistry,
        min_tier: TrustTier = TrustTier.D,
    ):
        self._registry = registry
        self._min_tier = min_tier

    def route(self, signal: ScreenerSignal) -> RouteDecision:
        channel = self._registry.by_alias(signal.source_channel)
        if channel is None:
            return RouteDecision(
                signal=signal,
                accepted=False,
                rejection_reason=f"unknown channel: {signal.source_channel}",
            )

        if not channel.enabled:
            return RouteDecision(
                signal=signal,
                channel=channel,
                accepted=False,
                rejection_reason="channel disabled",
            )

        if channel.trust_tier.value > self._min_tier.value:
            return RouteDecision(
                signal=signal,
                channel=channel,
                accepted=False,
                rejection_reason=(
                    f"trust tier {channel.trust_tier.value} below minimum {self._min_tier.value}"
                ),
            )

        expected = _SIGNAL_TYPE_TO_PARSER.get(signal.signal_type, [])
        if not any(p in channel.expected_parsers for p in expected):
            return RouteDecision(
                signal=signal,
                channel=channel,
                accepted=False,
                rejection_reason=(
                    f"signal type {signal.signal_type.value} not in expected parsers "
                    f"{channel.expected_parsers}"
                ),
            )

        meta = {}
        if signal.category and channel.categories:
            if signal.category.lower() not in {c.lower() for c in channel.categories}:
                meta["category_mismatch"] = (
                    f"category '{signal.category}' not in channel categories {channel.categories}"
                )

        return RouteDecision(
            signal=signal,
            channel=channel,
            accepted=True,
            metadata=meta,
        )

    def route_batch(self, signals: list[ScreenerSignal]) -> list[RouteDecision]:
        return [self.route(s) for s in signals]

    @property
    def registry(self) -> ChannelRegistry:
        return self._registry

    @property
    def min_tier(self) -> TrustTier:
        return self._min_tier
