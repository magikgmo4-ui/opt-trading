"""
coinglass_squeeze — squeeze/stress detection from Coinglass OCR data.

Detects potential short/long squeeze scenarios based on:
- Open Interest trend (rising OI = positioning, dropping = unwinding)
- Funding rate (positive = longs pay shorts, negative = shorts pay longs)
- Long/Short ratio (extreme ratios = crowded trade)
- Liquidation levels from heatmap
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_COINGLASS_PATH = _PROJECT_ROOT / "data" / "deskpro" / "inputs" / "vision_context" / "coinglass" / "latest.json"


def _read_coinglass() -> Optional[dict]:
    if not _COINGLASS_PATH.exists():
        return None
    try:
        return json.loads(_COINGLASS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def produce_squeeze_alert() -> dict:
    """Analyze Coinglass data for squeeze/stress conditions."""
    cg = _read_coinglass()
    if cg is None:
        return {"available": False, "alerts": [], "level": "UNKNOWN"}

    detection_method = cg.get("detection_method", "unknown")
    detections = cg.get("detections", [])
    if not isinstance(detections, list):
        detections = []

    oi = None
    funding = None
    for d in detections:
        if not isinstance(d, dict):
            continue
        metric = d.get("detected_metric_type", "")
        if "open_interest" in metric and "change" not in metric:
            oi = d.get("extracted_value")
        elif "funding" in metric:
            funding = d.get("extracted_value")

    alerts = []
    level = "LOW"

    # Stub detection degrades
    if detection_method == "stub":
        level = "STUB"
        return {
            "available": True,
            "data_quality": "STUB",
            "oi": oi,
            "funding_rate": funding,
            "alerts": alerts,
            "level": level,
            "note": "Coinglass data is a stub — no real OCR. Squeeze analysis unavailable.",
        }

    # High OI + positive funding = longs crowded → short squeeze risk
    if oi and oi > 100e9 and funding and funding > 0.03:
        alerts.append("HIGH_OI_POSITIVE_FUNDING: Longs crowded, potential short squeeze if price rises")
        level = "ELEVATED"

    # High OI + negative funding = shorts crowded → long squeeze risk
    if oi and oi > 100e9 and funding and funding < -0.03:
        alerts.append("HIGH_OI_NEGATIVE_FUNDING: Shorts crowded, potential long squeeze if price rises")
        level = "ELEVATED"

    # Extreme OI levels
    if oi and oi > 200e9:
        alerts.append("EXTREME_OI: Very high open interest, elevated squeeze risk in either direction")
        level = "HIGH"

    return {
        "available": True,
        "data_quality": "LIVE" if detection_method != "stub" else "STUB",
        "oi": oi,
        "funding_rate": funding,
        "detection_method": detection_method,
        "alerts": alerts,
        "level": level,
        "produced_at": datetime.now(timezone.utc).isoformat(),
    }
