from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Detection:
    detected_metric_type: str
    extracted_value: Optional[float]
    unit: str
    confidence: float
    evidence_ref: str
    notes: str = ""


@dataclass
class VisionRefs:
    raw_screenshot: str
    normalized: str
    latest: str
    events: str


@dataclass
class VisionContextCoinglassV1:
    contract_version: str
    input_class: str
    source_id: str
    screenshot_ts: str
    symbol: str
    timeframe: str
    board: str
    page: str
    freshness_state: str
    detections: List[Detection]
    refs: VisionRefs
    warnings: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if self.contract_version != "v1":
            raise ValueError(f"contract_version must be 'v1', got {self.contract_version!r}")

        if self.input_class != "vision_context.coinglass.v1":
            raise ValueError(
                f"input_class must be 'vision_context.coinglass.v1', got {self.input_class!r}"
            )

        for i, det in enumerate(self.detections):
            if det.confidence < 0 or det.confidence > 1:
                raise ValueError(
                    f"detections[{i}].confidence must be in [0,1], got {det.confidence}"
                )

            if det.confidence < 0.5 and not self.warnings:
                raise ValueError(
                    f"detections[{i}].confidence < 0.5 requires at least one warning"
                )

            if det.extracted_value is not None and det.confidence == 0:
                raise ValueError(
                    f"detections[{i}].extracted_value is non-null but confidence=0 — BLOCKED"
                )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["detections"] = [asdict(det) for det in self.detections]
        d["refs"] = asdict(self.refs)
        return d

    def to_json(self, **kwargs) -> str:
        return json.dumps(self.to_dict(), **kwargs)
