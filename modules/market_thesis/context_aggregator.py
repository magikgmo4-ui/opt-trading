"""
Context aggregator — PR2.

Aggregates all source data into a normalized MarketContextInput
for a given symbol. This is the input to the future thesis_engine (PR3-PR5).

Never crashes — returns partial results even with missing sources.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from .source_readers import (
    NormalizedEvent,
    NormalizedMetrics,
    NormalizedSetup,
    NormalizedVision,
    read_events_cdp_jsonl,
    read_events_jsonl,
    read_market_metrics,
    read_multitf_analysis,
    read_multitf_scores,
    read_signal_event_dc,
    read_telegram_signals,
    read_telegram_signals_dc,
    read_vision_analysis,
    read_vision_coinglass,
)
from .source_status import (
    SourceStatus,
    SourceStatusSet,
    evaluate_overall_freshness,
)


# ── MarketContextInput ─────────────────────────────────────────────────────

@dataclass
class MarketContextInput:
    """Normalized input for a single symbol, aggregating all available sources.

    This is an internal structure — not the public market_thesis.v1 contract.
    It feeds into the thesis_engine (PR3-PR5) which produces MarketThesis.
    """

    symbol: str
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # Source tracking
    source_statuses: List[SourceStatus] = field(default_factory=list)
    missing_sources: List[str] = field(default_factory=list)
    stale_sources: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    freshness_summary: str = "missing"

    # Raw events (all sources)
    raw_events: List[NormalizedEvent] = field(default_factory=list)

    # Technical inputs
    technical_inputs: Dict[str, Any] = field(default_factory=dict)

    # Flow inputs
    flow_inputs: Optional[NormalizedMetrics] = None

    # News / signal inputs
    news_inputs: List[NormalizedEvent] = field(default_factory=list)

    # Priority / scoring inputs
    priority_inputs: List[NormalizedSetup] = field(default_factory=list)

    # Vision inputs
    vision_inputs: List[NormalizedVision] = field(default_factory=list)

    # Telegram specific
    telegram_inputs: List[NormalizedEvent] = field(default_factory=list)

    # Multi-TF raw data (passthrough for thesis engine)
    multitf_raw: Optional[Dict[str, Any]] = None

    @property
    def has_any_data(self) -> bool:
        return bool(
            self.raw_events
            or self.technical_inputs
            or self.flow_inputs
            or self.news_inputs
            or self.priority_inputs
            or self.vision_inputs
            or self.telegram_inputs
            or self.multitf_raw
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "generated_at": self.generated_at.isoformat(),
            "freshness_summary": self.freshness_summary,
            "missing_sources": self.missing_sources,
            "stale_sources": self.stale_sources,
            "errors": self.errors,
            "source_statuses": [s.to_dict() for s in self.source_statuses],
            "raw_events_count": len(self.raw_events),
            "technical_inputs_keys": list(self.technical_inputs.keys()),
            "flow_inputs_present": self.flow_inputs is not None,
            "news_inputs_count": len(self.news_inputs),
            "priority_setups_count": len(self.priority_inputs),
            "vision_inputs_count": len(self.vision_inputs),
            "telegram_inputs_count": len(self.telegram_inputs),
            "multitf_raw_present": self.multitf_raw is not None,
        }


# ── Aggregator ─────────────────────────────────────────────────────────────

def aggregate(symbol: str) -> MarketContextInput:
    """Aggregate all available sources for a single canonical symbol.

    Never crashes — each source is wrapped in try/except.
    Returns partial results even if no sources are available.

    Args:
        symbol: Canonical symbol (BTC, ETH, SOL, XRP, XAU, SPCX, NVDA, AVGO, MU)

    Returns:
        MarketContextInput with all normalized data.
    """
    ctx = MarketContextInput(symbol=symbol)
    all_statuses: List[SourceStatus] = []

    # ── Webhook events ─────────────────────────────────────────────────
    try:
        events, status = read_events_jsonl(symbol)
        ctx.raw_events.extend(events)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Webhook Events", "webhook_event.v1", str(exc)))

    # ── CDP events ─────────────────────────────────────────────────────
    try:
        cdp_events, status = read_events_cdp_jsonl(symbol)
        ctx.raw_events.extend(cdp_events)
        ctx.news_inputs.extend(cdp_events)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("CDP Events", "signal_event.v1", str(exc)))

    # ── Market metrics ─────────────────────────────────────────────────
    try:
        metrics, status = read_market_metrics(symbol)
        if metrics is not None:
            ctx.flow_inputs = metrics
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Market Metrics", "market_metrics.v1", str(exc)))

    # ── Multi-TF analysis ──────────────────────────────────────────────
    try:
        multitf, status = read_multitf_analysis(symbol)
        if multitf is not None:
            ctx.multitf_raw = multitf
            ctx.technical_inputs = multitf
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Multi-TF Analysis", "multitf_analysis_input.v1", str(exc)))

    # ── Multi-TF scores ────────────────────────────────────────────────
    try:
        setups, status = read_multitf_scores(symbol)
        ctx.priority_inputs.extend(setups)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Multi-TF Scores", "multitf_setup_score.v1", str(exc)))

    # ── Vision Coinglass ───────────────────────────────────────────────
    try:
        vision_cg, status = read_vision_coinglass(symbol)
        if vision_cg is not None:
            ctx.vision_inputs.append(vision_cg)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Vision Coinglass", "vision_context.coinglass.v1", str(exc)))

    # ── Vision Analysis ────────────────────────────────────────────────
    try:
        vision_an, status = read_vision_analysis(symbol)
        if vision_an is not None:
            ctx.vision_inputs.append(vision_an)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Vision Analysis", "vision_analysis.v1", str(exc)))

    # ── Telegram signals ───────────────────────────────────────────────
    try:
        tg_events, status = read_telegram_signals(symbol)
        ctx.telegram_inputs.extend(tg_events)
        ctx.news_inputs.extend(tg_events)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Telegram Signals", "telegram_signal.v1", str(exc)))

    # ── Telegram signals DC ────────────────────────────────────────────
    try:
        tg_dc_events, status = read_telegram_signals_dc(symbol)
        ctx.telegram_inputs.extend(tg_dc_events)
        ctx.news_inputs.extend(tg_dc_events)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Telegram Signals DC", "telegram_signals.v1", str(exc)))

    # ── Signal events DC ───────────────────────────────────────────────
    try:
        sig_events, status = read_signal_event_dc(symbol)
        ctx.raw_events.extend(sig_events)
        ctx.news_inputs.extend(sig_events)
        all_statuses.append(status)
    except Exception as exc:
        all_statuses.append(_error_status("Signal Events DC", "signal_event.v1", str(exc)))

    # ── Finalize statuses ──────────────────────────────────────────────
    ctx.source_statuses = all_statuses
    ctx.missing_sources = [s.name for s in all_statuses if s.state == "missing"]
    ctx.stale_sources = [s.name for s in all_statuses if s.state in ("stale", "expired")]
    ctx.errors = [f"{s.name}: {s.error_message}" for s in all_statuses if s.state == "error" and s.error_message]
    ctx.freshness_summary = evaluate_overall_freshness(all_statuses)

    return ctx


def _error_status(name: str, contract: str, error: str) -> SourceStatus:
    return SourceStatus(name=name, contract=contract, state="error", error_message=error)
