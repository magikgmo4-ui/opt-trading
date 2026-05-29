from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from ..parser import (
    ScreenerSignal,
    SignalType,
    parse_trade_setup,
    parse_news_alert,
    parse_alpha_signal,
)
from ..parser.signal_normalizer import classify_raw_text
from ..registry import ChannelRegistry, TrustTier, load_channel_registry
from ..router import FilterRouter, RouteDecision
from ..signal import produce_screener_signal, adapt_to_telegram_claim, ScreenerProducedSignal


@dataclass
class PipelineResult:
    raw_text: str
    channel_alias: str
    signal: Optional[ScreenerSignal] = None
    route: Optional[RouteDecision] = None
    produced: Optional[ScreenerProducedSignal] = None
    claim: Optional[dict] = None
    error: Optional[str] = None

    @property
    def succeeded(self) -> bool:
        return self.error is None and self.claim is not None


class ScreenerPipeline:
    def __init__(
        self,
        registry: Optional[ChannelRegistry] = None,
        min_tier: TrustTier = TrustTier.D,
    ):
        self._registry = registry or load_channel_registry()
        self._router = FilterRouter(self._registry, min_tier=min_tier)

    def run(
        self,
        raw_text: str,
        channel_alias: str,
    ) -> PipelineResult:
        result = PipelineResult(raw_text=raw_text, channel_alias=channel_alias)

        signal_type_str = classify_raw_text(raw_text)
        if signal_type_str is None:
            result.error = "unparseable: raw_text does not match any parser"
            return result

        signal_type = SignalType(signal_type_str)

        parser_map = {
            SignalType.TRADE: parse_trade_setup,
            SignalType.NEWS: parse_news_alert,
            SignalType.ALPHA: parse_alpha_signal,
        }
        parser = parser_map[signal_type]
        signal = parser(raw_text, source_channel=channel_alias)
        if signal is None:
            result.error = f"parse failed: {signal_type_str} parser returned None"
            return result

        result.signal = signal

        route = self._router.route(signal)
        result.route = route
        if not route.accepted:
            result.error = f"rejected: {route.rejection_reason}"
            return result

        produced = produce_screener_signal(signal)
        result.produced = produced

        claim = adapt_to_telegram_claim(produced, channel_id=channel_alias)
        result.claim = claim

        return result

    def run_batch(
        self,
        inputs: list[tuple[str, str]],
    ) -> list[PipelineResult]:
        return [self.run(raw_text, alias) for raw_text, alias in inputs]

    @property
    def router(self) -> FilterRouter:
        return self._router
