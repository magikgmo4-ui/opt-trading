#!/usr/bin/env python3
"""Coinglass headless vision capture — staging entry point.

Usage:
    VISION_BOT_ENABLED=true python scripts/run_vision_capture.py
    VISION_BOT_ENABLED=true python scripts/run_vision_capture.py --validate
    VISION_BOT_ENABLED=true python scripts/run_vision_capture.py --validate --required 3

Environment:
    VISION_BOT_ENABLED=true   Required gate — refuses to run if not set.
    LOG_LEVEL=DEBUG            Optional verbose logging.

Requires playwright:
    pip install playwright && playwright install chromium

Staging gate: run with --validate after each capture.
Production: only activate after 3 consecutive --validate PASS.
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

# Ensure repo root is on path when run as script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from modules.env.env import load_env, ensure_dirs
from modules.vision.coinglass.ai_extraction import make_ai_extraction_fn
from modules.vision.coinglass.playwright_capture import make_playwright_browser_fn
from modules.vision.coinglass.runner import run_capture
from modules.vision.coinglass.staging_validator import validate_staging_runs

_LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=_LOG_LEVEL, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger("run_vision_capture")


def cmd_capture(args: argparse.Namespace) -> int:
    logger.info("starting capture (symbol=%s timeframe=%s)", args.symbol, args.timeframe)
    browser_fn = make_playwright_browser_fn(wait_ms=args.wait_ms)
    extraction_fn = make_ai_extraction_fn()  # no-op if VISION_AI_PROVIDER not set
    try:
        ctx = run_capture(
            browser_fn=browser_fn,
            extraction_fn=extraction_fn,
            symbol=args.symbol,
            timeframe=args.timeframe,
        )
    except RuntimeError as exc:
        logger.error("capture failed: %s", exc)
        return 1
    logger.info(
        "capture DONE — %d detections, freshness=%s",
        len(ctx.detections), ctx.freshness_state,
    )
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    report = validate_staging_runs(required_passes=args.required)
    print(f"[validate] {report.message}")
    for r in report.results:
        status = "PASS" if r.passed else "FAIL"
        print(f"  {r.screenshot_ts}  {status}  {r.reason}")
    return 0 if report.ok else 1


def main() -> int:
    load_env()
    ensure_dirs()

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--validate", action="store_true", help="validate staging runs instead of capturing")
    parser.add_argument("--required", type=int, default=3, help="consecutive PASS runs required (default: 3)")
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--timeframe", default="1H")
    parser.add_argument("--wait-ms", type=int, default=4000, dest="wait_ms", help="Playwright wait after page load (ms)")
    args = parser.parse_args()

    if args.validate:
        return cmd_validate(args)
    return cmd_capture(args)


if __name__ == "__main__":
    sys.exit(main())
