from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

from modules.desk_pro.models import Metric

VISION_CONTEXT_LATEST = Path(
    "data/deskpro/inputs/vision_context/coinglass/latest.json"
)

_METRIC_UNITS = {
    "liquidations_long": "USD",
    "liquidations_short": "USD",
    "long_short_ratio": "",
    "open_interest": "USD",
    "liquidation_heatmap_level": "USD",
}


def _confidence_to_quality(confidence: float) -> float:
    if confidence >= 0.85:
        return 0.95
    if confidence >= 0.60:
        return 0.70
    return 0.30


def read_vision_context_coinglass(path: Optional[Path] = None) -> List[Metric]:
    """Read vision_context.coinglass.v1 latest.json and return Desk Pro Metric objects.

    Returns empty list if file absent, malformed, or wrong input_class.
    Never raises. Never writes to market_metrics/ or any other path.
    """
    p = path or VISION_CONTEXT_LATEST
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []

    if data.get("input_class") != "vision_context.coinglass.v1":
        return []

    symbol = data.get("symbol", "UNKNOWN")
    source = data.get("source_id", "coinglass_headless_bot")
    freshness = data.get("freshness_state", "unknown")
    detections = data.get("detections", [])

    result: List[Metric] = []
    for det in detections:
        value = det.get("extracted_value")
        if value is None:
            continue
        confidence = det.get("confidence", 0.0)
        metric_type = det.get("detected_metric_type", "")
        quality = _confidence_to_quality(confidence)
        result.append(
            Metric(
                source=source,
                asset=symbol,
                metric=metric_type,
                value=value,
                unit=_METRIC_UNITS.get(metric_type, ""),
                window="vision",
                quality=quality,
                notes=f"vision_context.coinglass.v1 {freshness} conf={confidence:.2f}",
            )
        )

    return result
