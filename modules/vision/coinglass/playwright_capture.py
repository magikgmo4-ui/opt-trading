from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from modules.vision.coinglass.headless_capture import BrowserFn

logger = logging.getLogger(__name__)

_DEFAULT_VIEWPORT = {"width": 1440, "height": 900}
_DEFAULT_WAIT_MS = 4000
_GOTO_TIMEOUT_MS = 30_000
_USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
_LAUNCH_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
    "--disable-dev-shm-usage",
]


def make_playwright_browser_fn(
    wait_ms: int = _DEFAULT_WAIT_MS,
    viewport: dict | None = None,
) -> BrowserFn:
    """Return a BrowserFn that captures a screenshot via Playwright headless Chromium.

    Requires: pip install playwright && playwright install chromium
    Raises RuntimeError at call time if playwright is not installed.
    """
    vp = viewport or _DEFAULT_VIEWPORT

    def _capture(url: str, dest_dir: Path, ts: datetime) -> Path:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError(
                "playwright not installed — run: "
                "pip install playwright && playwright install chromium"
            ) from exc

        tag = ts.strftime("%Y%m%d_%H%M%S")
        dest = dest_dir / f"screenshot_{tag}.png"
        logger.info("playwright: opening %s", url)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=_LAUNCH_ARGS)
            try:
                ctx = browser.new_context(viewport=vp, user_agent=_USER_AGENT)
                page = ctx.new_page()
                page.goto(url, wait_until="networkidle", timeout=_GOTO_TIMEOUT_MS)
                page.wait_for_timeout(wait_ms)
                page.screenshot(path=str(dest), full_page=False)
                logger.info("playwright: screenshot written %s (%d bytes)", dest, dest.stat().st_size)
            finally:
                ctx.close()
                browser.close()
        return dest

    return _capture
