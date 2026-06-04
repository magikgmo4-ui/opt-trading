from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class VerdictChecklistItem:
    item: str
    status: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class VerdictComposite:
    btc_bias: str = "UNKNOWN"
    macro_regime: str = "UNKNOWN"
    alignment: str = "UNKNOWN"
    overall_bias: str = "UNKNOWN"
    confidence: str = "UNKNOWN"
    score: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class AnalysisVerdict:
    contract: str
    verdict_id: str
    produced_at: str
    freshness_state: str
    bundles_used: list[str]
    composite: dict
    checklist: list[dict]
    warnings: list[str] = field(default_factory=list)
    missing_inputs: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
