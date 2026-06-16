"""
Executive Intelligence models — PR1.

Three core contracts:
  - MarketRegime: detected market state (risk-on/off, expansion, panic, etc.)
  - ExecutiveState: global market snapshot (leaders, risks, changes)
  - ExecutiveBriefing: synthesized briefing for DeskPro + Voice

All read-only. No trade execution.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


# ── Market Regime ──────────────────────────────────────────────────────────

RegimeType = Literal[
    "risk_on", "risk_off",
    "expansion", "compression",
    "distribution", "accumulation",
    "panic", "recovery",
    "unknown",
]


class RegimeEvidence(BaseModel):
    """Evidence backing a market regime classification."""

    dxy_trend: str = Field(default="unknown", description="DXY trend: bullish, bearish, neutral")
    vix_level: str = Field(default="unknown", description="VIX: low, normal, elevated, high")
    spy_trend: str = Field(default="unknown", description="SPY trend")
    btc_dominance: Optional[float] = Field(default=None, description="BTC.D percentage")
    fear_greed: Optional[int] = Field(default=None, ge=0, le=100)
    correlation_matrix: dict = Field(default_factory=dict, description="Key cross-asset correlations")
    asset_count_bullish: int = Field(default=0, description="Number of assets with bullish thesis")
    asset_count_bearish: int = Field(default=0, description="Number of assets with bearish thesis")
    volatility_regime: str = Field(default="unknown", description="low, normal, high, extreme")


class MarketRegime(BaseModel):
    """Detected market regime with confidence and evidence."""

    contract: Literal["market_regime.v1"] = Field(
        default="market_regime.v1", serialization_alias="schema",
    )
    regime: RegimeType = Field(default="unknown")
    confidence: int = Field(default=0, ge=0, le=100)
    risk_score: int = Field(default=50, ge=0, le=100, description="0=no risk, 100=extreme risk")
    evidence: RegimeEvidence = Field(default_factory=RegimeEvidence)
    narrative: str = Field(default="", description="French narrative describing the regime")

    # Transition hints
    next_likely_regime: Optional[RegimeType] = Field(default=None)
    transition_probability: int = Field(default=0, ge=0, le=100)

    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ── Cross-Asset ────────────────────────────────────────────────────────────

class AssetInfluence(BaseModel):
    """Influence relationship between two assets."""

    source: str = Field(..., description="Leader / parent asset")
    target: str = Field(..., description="Follower / child asset")
    correlation: float = Field(default=0.0, ge=-1.0, le=1.0)
    influence_score: int = Field(default=0, ge=0, le=100)
    direction: str = Field(default="same", description="same, opposite, independent")
    evidence: str = Field(default="", description="Why this relationship exists")


class LeaderBoardEntry(BaseModel):
    """An asset's position on the leaderboard."""

    symbol: str = Field(...)
    rank: int = Field(default=0, ge=0)
    direction: str = Field(default="neutral")
    confidence: int = Field(default=0, ge=0, le=100)
    reliability: int = Field(default=0, ge=0, le=100)
    momentum_score: int = Field(default=0, ge=0, le=100)
    change_24h: Optional[float] = Field(default=None, description="Price change 24h %")
    is_leader: bool = Field(default=False)
    is_laggard: bool = Field(default=False)


# ── Changes ────────────────────────────────────────────────────────────────

class DetectedChange(BaseModel):
    """A change detected between two market states."""

    symbol: str = Field(default="market", description="Symbol or 'market' for global changes")
    field: str = Field(..., description="What changed: direction, confidence, regime, leadership")
    previous: str = Field(default="")
    current: str = Field(default="")
    magnitude: str = Field(default="moderate", description="minor, moderate, major")
    description: str = Field(default="", description="French description of the change")
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ── Top Items ──────────────────────────────────────────────────────────────

class TopOpportunity(BaseModel):
    """A top market opportunity."""

    symbol: str = Field(...)
    direction: str = Field(...)
    confidence: int = Field(default=0, ge=0, le=100)
    reliability: int = Field(default=0, ge=0, le=100)
    score: int = Field(default=0, ge=0, le=100, description="Composite opportunity score")
    reason: str = Field(default="")


class TopRisk(BaseModel):
    """A top market risk."""

    symbol: str = Field(default="market")
    category: str = Field(default="concentration")
    severity: str = Field(default="moderate")
    score: int = Field(default=0, ge=0, le=100)
    description: str = Field(default="")


# ── Executive State ────────────────────────────────────────────────────────

class ExecutiveState(BaseModel):
    """Complete global market intelligence snapshot."""

    contract: Literal["executive_state.v1"] = Field(
        default="executive_state.v1", serialization_alias="schema",
    )

    # Identity
    snapshot_id: str = Field(..., description="Unique snapshot ID")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ttl_seconds: int = Field(default=120, ge=30, le=600)

    # Market state
    regime: Optional[MarketRegime] = Field(default=None)

    # Cross-asset
    influences: List[AssetInfluence] = Field(default_factory=list)
    leaders: List[LeaderBoardEntry] = Field(default_factory=list)

    # Top items
    top_opportunities: List[TopOpportunity] = Field(default_factory=list)
    top_risks: List[TopRisk] = Field(default_factory=list)

    # Changes
    changes: List[DetectedChange] = Field(default_factory=list)

    # Confidence
    overall_confidence: int = Field(default=50, ge=0, le=100)
    source_count: int = Field(default=0, description="Number of individual theses used")

    # Freshness
    freshness: str = Field(default="unknown", description="fresh, stale, partial, expired")


# ── Executive Briefing ─────────────────────────────────────────────────────

class ExecutiveBriefing(BaseModel):
    """Human-readable executive briefing for DeskPro + Voice."""

    contract: Literal["executive_briefing.v1"] = Field(
        default="executive_briefing.v1", serialization_alias="schema",
    )

    briefing_id: str = Field(..., description="Unique briefing ID")
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Market summary
    market_regime: str = Field(default="unknown")
    regime_confidence: int = Field(default=0, ge=0, le=100)
    overall_confidence: int = Field(default=50, ge=0, le=100)

    # Leaders and laggards
    leaders: List[str] = Field(default_factory=list, description="Top performing assets")
    laggards: List[str] = Field(default_factory=list, description="Underperforming assets")

    # What's happening
    summary: str = Field(default="", description="2-3 sentence French summary")
    what_changed: str = Field(default="", description="What changed since last briefing")
    what_to_watch: str = Field(default="", description="What to monitor going forward")

    # Risks and opportunities
    top_risks: List[str] = Field(default_factory=list)
    top_opportunities: List[str] = Field(default_factory=list)

    # Voice
    voice_one_liner: str = Field(default="", description="Single-line French voice summary (<300 chars)")
    voice_briefing: str = Field(default="", description="Full French voice briefing (<600 chars)")


# ── Canonical fixtures ─────────────────────────────────────────────────────

CANONICAL_REGIME = MarketRegime(
    regime="risk_on",
    confidence=75,
    risk_score=35,
    evidence=RegimeEvidence(
        dxy_trend="bearish",
        vix_level="low",
        spy_trend="bullish",
        btc_dominance=58.0,
        fear_greed=65,
        asset_count_bullish=6,
        asset_count_bearish=2,
        volatility_regime="normal",
    ),
    narrative="Régime Risk-On confirmé. DXY baissier, VIX bas, SPY haussier. 6 actifs sur 9 en biais haussier.",
    next_likely_regime="expansion",
    transition_probability=60,
)

CANONICAL_EXECUTIVE_STATE = ExecutiveState(
    snapshot_id="exec_snap_20260615T120000Z",
    regime=CANONICAL_REGIME,
    influences=[
        AssetInfluence(source="BTC", target="ETH", correlation=0.85, influence_score=80, direction="same", evidence="Corrélation BTC-ETH historiquement forte."),
        AssetInfluence(source="BTC", target="SOL", correlation=0.72, influence_score=65, direction="same", evidence="SOL suit BTC avec bêta élevé."),
        AssetInfluence(source="DXY", target="XAU", correlation=-0.60, influence_score=70, direction="opposite", evidence="Gold inversement corrélé au dollar."),
        AssetInfluence(source="SPY", target="NVDA", correlation=0.78, influence_score=75, direction="same", evidence="NVDA fortement corrélée au marché actions."),
    ],
    leaders=[
        LeaderBoardEntry(symbol="BTC", rank=1, direction="bullish", confidence=75, reliability=82, momentum_score=70, is_leader=True),
        LeaderBoardEntry(symbol="NVDA", rank=2, direction="bullish", confidence=80, reliability=78, momentum_score=85, is_leader=True),
    ],
    top_opportunities=[
        TopOpportunity(symbol="BTC", direction="bullish", confidence=75, reliability=82, score=78, reason="Contexte macro favorable + fiabilité élevée"),
        TopOpportunity(symbol="NVDA", direction="bullish", confidence=80, reliability=78, score=79, reason="Momentum IA fort + semiconducteurs en expansion"),
    ],
    top_risks=[
        TopRisk(symbol="market", category="macro", severity="high", score=65, description="Renforcement du dollar si la Fed devient hawkish"),
        TopRisk(symbol="BTC", category="concentration", severity="moderate", score=55, description="Crowding long sur BTC. Risque de correction si support cassé."),
    ],
    changes=[
        DetectedChange(symbol="market", field="regime", previous="compression", current="risk_on", magnitude="major", description="Le régime est passé de compression à risk-on."),
        DetectedChange(symbol="SPCX", field="direction", previous="neutral", current="bullish", magnitude="moderate", description="SPCX passe en biais haussier avec momentum positif."),
    ],
    overall_confidence=72,
    source_count=9,
    freshness="fresh",
)

CANONICAL_BRIEFING = ExecutiveBriefing(
    briefing_id="brief_20260615T120000Z",
    market_regime="risk_on",
    regime_confidence=75,
    overall_confidence=72,
    leaders=["BTC", "NVDA", "SPCX"],
    laggards=["AVGO", "XRP"],
    summary="Le marché reste en régime Risk-On. BTC et le secteur semiconducteurs mènent la tendance haussière. Le dollar faible soutient l'or et les actifs risqués.",
    what_changed="Le régime est passé de compression à risk-on. SPCX repasse en biais haussier.",
    what_to_watch="Surveiller le DXY : un rebond du dollar pourrait inverser la tendance. Attention au crowding long sur BTC.",
    top_risks=["Renforcement du dollar (hawkish Fed)", "Crowding long BTC", "Volatilité SPCX"],
    top_opportunities=["BTC soutenu par le régime risk-on", "NVDA momentum IA", "Gold couverture dollar faible"],
    voice_one_liner="Marché en régime Risk-On. BTC et NVDA en tête. 6 actifs sur 9 haussiers. Principaux risques : dollar et crowding long.",
    voice_briefing="Régime de marché Risk-On confirmé avec 75% de confiance. Les leaders sont BTC, NVDA et SPCX. Les actifs en retard sont AVGO et XRP. Le régime est passé de compression à risk-on. Le principal risque est un éventuel renforcement du dollar. Surveillance recommandée sur tous les actifs.",
)
