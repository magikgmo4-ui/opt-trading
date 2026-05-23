from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional

from modules.vision.coinglass.vision_context_v1 import Detection

logger = logging.getLogger(__name__)

CONFIDENCE_THRESHOLD = 0.60
STALE_HOURS = 4

ExtractionFn = Callable[[Path], List[Detection]]


def _screenshot_age_hours(screenshot_ts: datetime) -> float:
    now = datetime.now(tz=timezone.utc)
    ts = screenshot_ts if screenshot_ts.tzinfo else screenshot_ts.replace(tzinfo=timezone.utc)
    return (now - ts).total_seconds() / 3600


def parse_screenshot(
    image_path: Path,
    screenshot_ts: datetime,
    extraction_fn: ExtractionFn,
    confidence_threshold: float = CONFIDENCE_THRESHOLD,
) -> tuple[List[Detection], List[str], str]:
    """Return (detections, warnings, freshness_state).

    extraction_fn is injected — real impl uses OCR/AI, mock uses fixtures.
    Returns empty list on any failure (silent degradation).
    """
    if not image_path.exists():
        logger.warning("screenshot not found: %s", image_path)
        return [], [], "unknown"

    try:
        raw_detections = extraction_fn(image_path)
    except Exception:
        logger.exception("extraction_fn failed for %s", image_path)
        return [], [], "unknown"

    warnings: List[str] = []
    filtered: List[Detection] = []

    for det in raw_detections:
        if det.confidence < confidence_threshold:
            warnings.append(
                f"{det.detected_metric_type}: confidence {det.confidence:.2f} < "
                f"{confidence_threshold} — value set to null"
            )
            filtered.append(Detection(
                detected_metric_type=det.detected_metric_type,
                extracted_value=None,
                unit=det.unit,
                confidence=det.confidence,
                evidence_ref=det.evidence_ref,
                notes=det.notes or f"confidence {det.confidence:.2f} below threshold",
            ))
        else:
            filtered.append(det)

    age_h = _screenshot_age_hours(screenshot_ts)
    freshness_state = "stale" if age_h >= STALE_HOURS else "fresh"

    return filtered, warnings, freshness_state
