"""
market_thesis.v1 — Pydantic v2 models.

Canonical contract for the unified market thesis per asset.
Read-only — no trade execution, no broker integration.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


# ── Enums as Literals ────────────────────────────────────────────────────

MacroRegime = Literal["risk_on", "risk_off", "neutral", "unknown"]
TrendDirection = Literal["bullish", "bearish", "neutral", "unknown"]
VIXState = Literal["low", "normal", "elevated", "high", "unknown"]
MarketPhase = Literal["accumulation", "markup", "distribution", "markdown", "unknown"]
HTFLTFBias = Literal["bullish", "bearish", "neutral"]
Alignment = Literal["aligned_bullish", "aligned_bearish", "divergent", "neutral"]
Sentiment = Literal["positive", "neutral", "negative", "unknown"]
Severity = Literal["high", "moderate", "low"]
SourceStatus = Literal["used", "missing", "stale"]
FreshnessState = Literal["fresh", "stale", "partial", "expired"]


# ── Models ───────────────────────────────────────────────────────────────

class ThesisMetadata(BaseModel):
    """Metadata for a market thesis instance."""

    thesis_id: str = Field(
        ...,
        description="Unique thesis identifier, format: thesis_{SYM}_{ISO8601}",
    )
    contract: Literal["market_thesis.v1"] = Field(
        default="market_thesis.v1",
        serialization_alias="schema",
        description="Schema version discriminator",
    )
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of thesis generation",
    )
    ttl_seconds: int = Field(
        default=300,
        ge=10,
        le=3600,
        description="Cache validity duration in seconds (10–3600)",
    )
    version: str = Field(
        default="1.0.0",
        description="Engine version",
    )


class MarketContext(BaseModel):
    """Macro and regime context for the asset."""

    macro_regime: MacroRegime = Field(
        default="unknown",
        description="Overall risk environment",
    )
    dxy_trend: TrendDirection = Field(
        default="unknown",
        description="DXY trend direction",
    )
    vix_state: VIXState = Field(
        default="unknown",
        description="VIX volatility state",
    )
    spy_trend: TrendDirection = Field(
        default="unknown",
        description="SPY trend direction",
    )
    market_phase: MarketPhase = Field(
        default="unknown",
        description="Market cycle phase (Wyckoff)",
    )
    narrative: str = Field(
        default="",
        description="French narrative describing the macro context",
    )


class TechnicalSection(BaseModel):
    """Technical analysis section."""

    htf_bias: HTFLTFBias = Field(
        default="neutral",
        description="Higher timeframe bias (D1/W1)",
    )
    ltf_bias: HTFLTFBias = Field(
        default="neutral",
        description="Lower timeframe bias (H4/H1)",
    )
    alignment: Alignment = Field(
        default="neutral",
        description="HTF/LTF alignment",
    )
    key_support: List[float] = Field(
        default_factory=list,
        description="Key support levels, sorted nearest to farthest",
    )
    key_resistance: List[float] = Field(
        default_factory=list,
        description="Key resistance levels, sorted nearest to farthest",
    )
    vwap: Optional[float] = Field(
        default=None,
        description="VWAP level",
    )
    active_setups: List[str] = Field(
        default_factory=list,
        description="Active setup identifiers currently in play",
    )
    narrative: str = Field(
        default="",
        description="French narrative describing technical structure",
    )


class FlowSection(BaseModel):
    """Capital flow and derivatives positioning section."""

    open_interest: Optional[float] = Field(
        default=None,
        description="Total open interest in USD",
    )
    oi_change_24h_pct: Optional[float] = Field(
        default=None,
        description="Open interest 24h change in percent",
    )
    funding_rate: Optional[float] = Field(
        default=None,
        description="Current funding rate",
    )
    long_short_ratio: Optional[float] = Field(
        default=None,
        description="Account long/short ratio",
    )
    liquidations_long: Optional[float] = Field(
        default=None,
        description="Long liquidations 24h in USD",
    )
    liquidations_short: Optional[float] = Field(
        default=None,
        description="Short liquidations 24h in USD",
    )
    etf_flow: Optional[str] = Field(
        default=None,
        description="ETF flow direction (inflow/outflow/flat)",
    )
    narrative: str = Field(
        default="",
        description="French narrative describing flow positioning",
    )


class NewsSection(BaseModel):
    """News and sentiment section."""

    sentiment: Sentiment = Field(
        default="unknown",
        description="Overall news sentiment",
    )
    sentiment_score: float = Field(
        default=0.0,
        ge=-1.0,
        le=1.0,
        description="Sentiment score from -1 (negative) to 1 (positive)",
    )
    key_drivers: List[str] = Field(
        default_factory=list,
        description="Key news drivers impacting the asset",
    )
    narrative: str = Field(
        default="",
        description="French narrative describing news and sentiment",
    )


class RiskItem(BaseModel):
    """A single risk factor identified in the thesis."""

    category: str = Field(
        ...,
        description="Risk category: concentration, technical, event, regulatory, correlation",
    )
    severity: Severity = Field(
        ...,
        description="Risk severity level",
    )
    description: str = Field(
        ...,
        description="French description of the risk factor",
    )


class ProbabilitySet(BaseModel):
    """Directional probability decomposition.

    Invariant: bull + range + bear == 100
    """

    bull: int = Field(
        ...,
        ge=0,
        le=100,
        description="Probability of bullish outcome (0–100)",
    )
    range: int = Field(
        ...,
        ge=0,
        le=100,
        description="Probability of ranging outcome (0–100)",
    )
    bear: int = Field(
        ...,
        ge=0,
        le=100,
        description="Probability of bearish outcome (0–100)",
    )

    @model_validator(mode="after")
    def _total_must_equal_100(self) -> "ProbabilitySet":
        total = self.bull + self.range + self.bear
        if total != 100:
            raise ValueError(
                f"ProbabilitySet bull+range+bear must total 100, got {total} "
                f"(bull={self.bull}, range={self.range}, bear={self.bear})"
            )
        return self


class ActionPlan(BaseModel):
    """Action recommendation.

    Strictly monitor-only — no automated execution.
    """

    direction: Literal["bullish", "bearish", "neutral", "wait"] = Field(
        default="neutral",
        description="Directional bias",
    )
    readiness: Literal["monitor_only"] = Field(
        default="monitor_only",
        description="Always monitor_only — no auto execution permitted",
    )
    key_levels: List[str] = Field(
        default_factory=list,
        description="Key levels to watch with labels (entry, invalidation, target)",
    )
    narrative: str = Field(
        default="",
        description="French narrative describing the action recommendation",
    )
    voice_one_liner: str = Field(
        default="",
        description="Single-line French summary for voice TTS (< 200 chars)",
    )


class SourceRef(BaseModel):
    """Reference to a data source used in the thesis."""

    name: str = Field(
        ...,
        description="Human-readable source name",
    )
    contract: str = Field(
        ...,
        description="DC contract class (e.g. market_metrics.v1)",
    )
    status: SourceStatus = Field(
        ...,
        description="Source availability status",
    )
    age_minutes: Optional[float] = Field(
        default=None,
        description="Data age in minutes, if available",
    )


class FreshnessStatus(BaseModel):
    """Overall data freshness assessment."""

    overall: FreshnessState = Field(
        ...,
        description="Aggregate freshness state",
    )
    max_age_minutes: float = Field(
        default=0.0,
        ge=0,
        description="Age of the oldest source used",
    )
    source_count: int = Field(
        default=0,
        ge=0,
        description="Total number of source contracts evaluated",
    )
    fresh_count: int = Field(
        default=0,
        ge=0,
        description="Number of sources with fresh data",
    )


# ── Top-level Model ──────────────────────────────────────────────────────

class MarketThesis(BaseModel):
    """Complete market thesis for a single symbol.

    This is the canonical output of the Market Thesis Engine.
    Read-only — no trade execution, no broker integration.
    """

    metadata: ThesisMetadata = Field(
        ...,
        description="Thesis metadata (id, schema, timestamps)",
    )
    symbol: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Canonical symbol: BTC, ETH, SOL, XRP, XAU, SPCX, NVDA, AVGO, MU",
    )
    timeframe: str = Field(
        default="composite",
        description="Primary timeframe or 'composite' for multi-TF synthesis",
    )
    context: MarketContext = Field(
        default_factory=MarketContext,
        description="Macro and regime context",
    )
    technical: TechnicalSection = Field(
        default_factory=TechnicalSection,
        description="Technical analysis",
    )
    flow: FlowSection = Field(
        default_factory=FlowSection,
        description="Capital flows and derivatives positioning",
    )
    news: NewsSection = Field(
        default_factory=NewsSection,
        description="News and sentiment",
    )
    risks: List[RiskItem] = Field(
        default_factory=list,
        description="Identified risk factors",
    )
    probabilities: ProbabilitySet = Field(
        ...,
        description="Directional probability decomposition (must total 100)",
    )
    action: ActionPlan = Field(
        default_factory=ActionPlan,
        description="Action recommendation (monitor-only)",
    )
    sources: List[SourceRef] = Field(
        default_factory=list,
        description="Data sources used in this thesis",
    )
    freshness: FreshnessStatus = Field(
        ...,
        description="Data freshness assessment",
    )
    confidence: int = Field(
        ...,
        ge=0,
        le=100,
        description="Overall thesis confidence (0–100)",
    )


# ── Canonical BTC example (valid fixture) ─────────────────────────────────

CANONICAL_BTC_THESIS = MarketThesis(
    metadata=ThesisMetadata(
        thesis_id="thesis_BTC_20260615T120000Z",
        generated_at=datetime(2026, 6, 15, 12, 0, 0, tzinfo=timezone.utc),
        ttl_seconds=300,
    ),
    symbol="BTC",
    timeframe="composite",
    context=MarketContext(
        macro_regime="risk_on",
        dxy_trend="bearish",
        vix_state="low",
        spy_trend="bullish",
        market_phase="markup",
        narrative=(
            "Contexte macro favorable : DXY en baisse, VIX bas (<15), "
            "SPY haussier. Marché en phase de markup."
        ),
    ),
    technical=TechnicalSection(
        htf_bias="bullish",
        ltf_bias="bearish",
        alignment="divergent",
        key_support=[65000.0, 62000.0],
        key_resistance=[72000.0],
        vwap=66450.0,
        active_setups=["btc_vwap_reclaim"],
        narrative=(
            "Structure D1 haussière mais H4 bearish : divergence HTF/LTF. "
            "Prix sous VWAP. Support majeur à 65000, résistance à 72000."
        ),
    ),
    flow=FlowSection(
        open_interest=28_500_000_000.0,
        oi_change_24h_pct=2.1,
        funding_rate=0.0035,
        long_short_ratio=1.8,
        liquidations_long=45_000_000.0,
        liquidations_short=12_000_000.0,
        etf_flow="inflow",
        narrative=(
            "OI en hausse (+2.1%), funding positif, ratio L/S à 1.8. "
            "Liquidations longs dominantes. ETF inflows continus."
        ),
    ),
    news=NewsSection(
        sentiment="positive",
        sentiment_score=0.45,
        key_drivers=["ETF inflows record", "CPI lower than expected"],
        narrative=(
            "Sentiment news positif (score +0.45). ETF inflows et CPI bas "
            "soutiennent le biais haussier."
        ),
    ),
    risks=[
        RiskItem(
            category="concentration",
            severity="high",
            description="Crowding long élevé (L/S 1.8). Risque de cascade si support 65000 casse.",
        ),
        RiskItem(
            category="technical",
            severity="moderate",
            description="Divergence HTF/LTF. Invalidation à 65000.",
        ),
    ],
    probabilities=ProbabilitySet(bull=50, range=30, bear=20),
    action=ActionPlan(
        direction="bullish",
        readiness="monitor_only",
        key_levels=[
            "Entry: VWAP reclaim H1 > 66450",
            "Invalidation: 65000",
            "Target: 68000",
        ],
        narrative="Biais haussier modéré. Attendre confirmation VWAP H1.",
        voice_one_liner=(
            "BTC biais haussier modéré, attente confirmation. "
            "VWAP à 66450, support à 65000. Contexte macro favorable."
        ),
    ),
    sources=[
        SourceRef(name="Binance spot", contract="market_metrics.v1", status="used", age_minutes=3.2),
        SourceRef(name="MultiTF analysis", contract="multitf_analysis_input.v1", status="used", age_minutes=8.5),
        SourceRef(name="MultiTF scores", contract="multitf_setup_score.v1", status="used", age_minutes=8.5),
        SourceRef(name="Vision analysis", contract="vision_analysis.v1", status="used", age_minutes=5.1),
        SourceRef(name="Coinglass OCR", contract="vision_context.coinglass.v1", status="missing", age_minutes=None),
        SourceRef(name="Telegram signals", contract="telegram_signals.v1", status="used", age_minutes=2.0),
    ],
    freshness=FreshnessStatus(
        overall="fresh",
        max_age_minutes=8.5,
        source_count=6,
        fresh_count=5,
    ),
    confidence=55,
)
