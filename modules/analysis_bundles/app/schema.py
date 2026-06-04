from dataclasses import dataclass, field, asdict
from typing import Optional


VALID_FRESHNESS_STATES = {"FRESH", "STALE", "UNKNOWN", "HYPOTHESIS"}
VALID_BIAS = {"BULLISH", "BEARISH", "NEUTRAL", "UNKNOWN"}
VALID_REGIME = {
    "TRENDING", "RANGING", "SQUEEZE", "VOLATILE",
    "BREAKOUT_SIGNAL", "OI_FLAT", "LONG_SKEWED",
    "RISK_ON", "RISK_OFF", "RISK_ON_BROADENING",
    "UNKNOWN",
}
VALID_SQUEEZE = {"LOW", "MEDIUM", "ELEVATED", "HIGH", "UNKNOWN"}
VALID_CONFIDENCE = {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}


@dataclass
class BundleInput:
    source: str
    freshness: str
    produced_at: Optional[str] = None

    def to_dict(self) -> dict:
        d = {"source": self.source, "freshness": self.freshness}
        if self.produced_at is not None:
            d["produced_at"] = self.produced_at
        return d


@dataclass
class BundleAnalysis:
    timeframe: str = "UNKNOWN"
    bias_short_term: str = "UNKNOWN"
    bias_intraday: str = "UNKNOWN"
    regime: str = "UNKNOWN"
    squeeze_or_stress_level: str = "UNKNOWN"
    invalidation: Optional[str] = None
    confidence: str = "UNKNOWN"
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None}


@dataclass
class BundleOutput:
    contract: str
    bundle_id: str
    produced_at: str
    freshness_state: str
    assets: list[str]
    inputs: dict
    analysis: dict
    missing_inputs: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
