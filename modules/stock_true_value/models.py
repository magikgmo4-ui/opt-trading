"""Typed models for Stock True Value / SpaceX Intelligence scoring."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class SourceHealth:
    required_sources_available: int = 0
    optional_sources_available: int = 0
    missing_sources: tuple[str, ...] = ()
    stale_sources: tuple[str, ...] = ()
    data_conflicts: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True)
class ScoreSnapshot:
    ticker: str
    asof: datetime
    model_version: str
    universe: str

    fundamental_score: float | None = None
    valuation_score: float | None = None
    flow_score: float | None = None
    speculation_score: float | None = None
    surprise_score: float | None = None
    catalyst_score: float | None = None
    ecosystem_score: float | None = None

    true_value_score: float = 0.0
    hype_score: float = 0.0
    risk_score: float = 0.0
    confidence_score: float = 0.0
    final_score: float | None = None

    final_grade: str = "RESEARCH_REQUIRED"
    action_bias: str = "deep_research_required"
    flags: tuple[str, ...] = field(default_factory=tuple)
    positive_drivers: tuple[str, ...] = field(default_factory=tuple)
    negative_offsets: tuple[str, ...] = field(default_factory=tuple)
    source_health: SourceHealth = field(default_factory=SourceHealth)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ticker": self.ticker,
            "asof": self.asof.isoformat(),
            "model_version": self.model_version,
            "universe": self.universe,
            "fundamental_score": self.fundamental_score,
            "valuation_score": self.valuation_score,
            "flow_score": self.flow_score,
            "speculation_score": self.speculation_score,
            "surprise_score": self.surprise_score,
            "catalyst_score": self.catalyst_score,
            "ecosystem_score": self.ecosystem_score,
            "true_value_score": self.true_value_score,
            "hype_score": self.hype_score,
            "risk_score": self.risk_score,
            "confidence_score": self.confidence_score,
            "final_score": self.final_score,
            "final_grade": self.final_grade,
            "action_bias": self.action_bias,
            "flags": list(self.flags),
            "drivers": {
                "positive": list(self.positive_drivers),
                "negative": list(self.negative_offsets),
            },
            "source_health": {
                "required_sources_available": self.source_health.required_sources_available,
                "optional_sources_available": self.source_health.optional_sources_available,
                "missing_sources": list(self.source_health.missing_sources),
                "stale_sources": list(self.source_health.stale_sources),
                "data_conflicts": list(self.source_health.data_conflicts),
            },
        }
