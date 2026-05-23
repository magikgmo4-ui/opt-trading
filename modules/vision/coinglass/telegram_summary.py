from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

from modules.vision.coinglass.vision_context_v1 import Detection, VisionContextCoinglassV1

logger = logging.getLogger(__name__)

VISION_LATEST = Path("data/vision/coinglass/latest.json")

_HIGH_CONF = 0.85
_LOW_CONF = 0.60

_METRIC_LABELS = {
    "liquidations_long": "Liq Longs",
    "liquidations_short": "Liq Shorts",
    "long_short_ratio": "L/S Ratio",
    "open_interest": "Open Interest",
    "liquidation_heatmap_level": "Heatmap Level",
}


def _fmt_value(value: Optional[float], unit: str) -> str:
    if value is None:
        return "N/A"
    if unit == "USD":
        if value >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"
        if value >= 1_000:
            return f"${value / 1_000:.1f}K"
        return f"${value:.2f}"
    if unit == "%":
        return f"{value:.2f}%"
    return f"{value:.4g}"


def _conf_tag(confidence: float) -> str:
    if confidence >= _HIGH_CONF:
        return ""
    if confidence >= _LOW_CONF:
        return f" ⚠ conf={confidence:.0%}"
    return f" ✗ conf={confidence:.0%} (low)"


def format_vision_summary(ctx: VisionContextCoinglassV1) -> str:
    """Format a VisionContextCoinglassV1 as a plain-text Telegram summary.

    Values shown are exclusively those in ctx.detections — nothing invented.
    Confidence < 0.85 is flagged with a warning tag.
    """
    lines = [
        f"<b>Coinglass Vision</b> — {ctx.symbol} {ctx.timeframe}",
        f"Board: {ctx.board} | Page: {ctx.page}",
        f"Freshness: {ctx.freshness_state} | {ctx.screenshot_ts}",
        "",
    ]

    if not ctx.detections:
        lines.append("No detections.")
    else:
        for det in ctx.detections:
            label = _METRIC_LABELS.get(det.detected_metric_type, det.detected_metric_type)
            val_str = _fmt_value(det.extracted_value, det.unit)
            tag = _conf_tag(det.confidence)
            lines.append(f"• {label}: {val_str}{tag}")

    if ctx.warnings:
        lines.append("")
        lines.append("<i>Warnings:</i>")
        for w in ctx.warnings:
            lines.append(f"  – {w}")

    return "\n".join(lines)


def load_and_format(path: Optional[Path] = None) -> Optional[str]:
    """Load latest.json and return formatted summary, or None on any failure."""
    p = path or VISION_LATEST
    if not p.exists():
        logger.warning("vision latest.json not found: %s", p)
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        logger.exception("failed to read vision latest.json")
        return None

    if data.get("input_class") != "vision_context.coinglass.v1":
        logger.warning("unexpected input_class: %s", data.get("input_class"))
        return None

    try:
        detections_raw = data.get("detections", [])
        from modules.vision.coinglass.vision_context_v1 import Detection, VisionRefs
        detections = [Detection(**d) for d in detections_raw]
        refs_raw = data.get("refs", {})
        refs = VisionRefs(**refs_raw)
        ctx = VisionContextCoinglassV1(
            contract_version=data["contract_version"],
            input_class=data["input_class"],
            source_id=data["source_id"],
            screenshot_ts=data["screenshot_ts"],
            symbol=data["symbol"],
            timeframe=data["timeframe"],
            board=data["board"],
            page=data["page"],
            freshness_state=data["freshness_state"],
            detections=detections,
            refs=refs,
            warnings=data.get("warnings", []),
        )
    except Exception:
        logger.exception("failed to reconstruct VisionContextCoinglassV1")
        return None

    return format_vision_summary(ctx)
