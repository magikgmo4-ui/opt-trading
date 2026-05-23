from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Optional

from modules.vision.coinglass.headless_capture import BrowserFn, capture_screenshot
from modules.vision.coinglass.parser import ExtractionFn, parse_screenshot
from modules.vision.coinglass.vision_context_v1 import (
    Detection,
    VisionContextCoinglassV1,
    VisionRefs,
)

logger = logging.getLogger(__name__)

_VISION_DIR = Path("data/vision/coinglass")
_DESKPRO_INPUT = Path("data/deskpro/inputs/vision_context/coinglass/latest.json")

_ALLOWED_WRITE_ROOTS = (
    Path("data/vision/coinglass"),
    Path("data/deskpro/inputs/vision_context/coinglass"),
)


def _ts_tag(ts: datetime) -> str:
    return ts.strftime("%Y%m%d_%H%M%S")


def run_capture(
    browser_fn: BrowserFn,
    extraction_fn: ExtractionFn,
    symbol: str = "BTCUSDT",
    timeframe: str = "1H",
    board: str = "liquidations",
    page: str = "liquidation_heatmap",
    run_ts: Optional[datetime] = None,
) -> VisionContextCoinglassV1:
    """Full pipeline: capture → parse → build context → write files.

    Returns the VisionContextCoinglassV1 written. Raises RuntimeError if
    VISION_BOT_ENABLED is not set (gate from headless_capture).
    Never writes outside data/vision/coinglass/ and data/deskpro/inputs/vision_context/.
    """
    ts = run_ts or datetime.now(tz=timezone.utc)
    tag = _ts_tag(ts)

    raw_dir = _VISION_DIR / "raw"
    normalized_dir = _VISION_DIR / "normalized"
    for d in (raw_dir, normalized_dir, _DESKPRO_INPUT.parent):
        d.mkdir(parents=True, exist_ok=True)

    screenshot_path = capture_screenshot(browser_fn, dest_dir=raw_dir, ts=ts)

    detections, warnings, freshness_state = parse_screenshot(
        image_path=screenshot_path,
        screenshot_ts=ts,
        extraction_fn=extraction_fn,
    )

    refs = VisionRefs(
        raw_screenshot=str(screenshot_path),
        normalized=str(normalized_dir / f"vision_{tag}.json"),
        latest=str(_VISION_DIR / "latest.json"),
        events=str(_VISION_DIR / "events.jsonl"),
    )

    ctx = VisionContextCoinglassV1(
        contract_version="v1",
        input_class="vision_context.coinglass.v1",
        source_id="coinglass_headless_bot",
        screenshot_ts=ts.strftime("%Y-%m-%dT%H:%M:%SZ"),
        symbol=symbol,
        timeframe=timeframe,
        board=board,
        page=page,
        freshness_state=freshness_state,
        detections=detections,
        refs=refs,
        warnings=warnings,
    )
    ctx.validate()

    payload = ctx.to_json(indent=2)

    # Write normalized
    normalized_path = Path(refs.normalized)
    normalized_path.write_text(payload, encoding="utf-8")

    # Write latest
    latest_path = Path(refs.latest)
    latest_path.write_text(payload, encoding="utf-8")

    # Append to events
    events_path = Path(refs.events)
    with events_path.open("a", encoding="utf-8") as f:
        f.write(ctx.to_json() + "\n")

    # Write Desk Pro input (copy of latest)
    _DESKPRO_INPUT.write_text(payload, encoding="utf-8")

    logger.info(
        "run_capture DONE: %d detections, freshness=%s, warnings=%d",
        len(detections), freshness_state, len(warnings),
    )
    return ctx
