from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

logger = logging.getLogger(__name__)

COINGLASS_LIQUIDATIONS_URL = "https://www.coinglass.com/liquidations"

RAW_DIR = Path("data/vision/coinglass/raw")

# Callable[[url: str, dest_dir: Path, ts: datetime], Path]
BrowserFn = Callable[[str, Path, datetime], Path]


def _gate_check() -> None:
    if os.environ.get("VISION_BOT_ENABLED", "").lower() != "true":
        raise RuntimeError(
            "VISION_BOT_ENABLED is not set to 'true' — headless capture is gated. "
            "Set VISION_BOT_ENABLED=true to activate in staging."
        )


def capture_screenshot(
    browser_fn: BrowserFn,
    url: str = COINGLASS_LIQUIDATIONS_URL,
    dest_dir: Path = RAW_DIR,
    ts: datetime | None = None,
) -> Path:
    """Capture a Coinglass page screenshot using the injected browser_fn.

    Raises RuntimeError if VISION_BOT_ENABLED is not set (gate).
    browser_fn is injected — real impl uses Playwright, mock returns a fixture PNG.
    """
    _gate_check()
    ts = ts or datetime.now(tz=timezone.utc)
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = browser_fn(url, dest_dir, ts)
    if not path.exists() or path.stat().st_size == 0:
        raise RuntimeError(f"browser_fn produced an empty or missing file: {path}")
    logger.info("screenshot captured: %s (%d bytes)", path, path.stat().st_size)
    return path
