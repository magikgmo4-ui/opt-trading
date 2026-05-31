#!/usr/bin/env python3
"""
Pipeline orchestrator: capture → analyze → output → (optional) Telegram.
Usage:
  python3 scripts/run_vision_pipeline.py --profile profiles.btcusdt_poc.json --once
  python3 scripts/run_vision_pipeline.py --profile profiles.btcusdt_poc.json --telegram
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
HEADLESS_DIR = REPO_ROOT / "modules" / "bot_vision" / "headless_capture"
CAPTURE_SCRIPT = HEADLESS_DIR / "capture_headless.js"
ANALYZE_SCRIPT = HEADLESS_DIR / "scripts" / "analyze_capture.py"
VISION_INBOX = Path(os.getenv("BOT_VISION_OUT", str(REPO_ROOT / "data" / "vision_inbox")))


def find_latest_capture(inbox: Path) -> dict[str, Any] | None:
    if not inbox.exists():
        return None
    jsons = sorted(inbox.glob("screen_*.json"), key=os.path.getmtime, reverse=True)
    if not jsons:
        return None
    latest = jsons[0]
    try:
        meta = json.loads(latest.read_text(encoding="utf-8"))
    except Exception:
        return None

    png_name = meta.get("output_png", "")
    png_path = inbox / png_name if png_name else None

    if png_path and png_path.exists():
        meta["png_path"] = str(png_path)
    else:
        alt_png = latest.with_suffix(".png")
        if alt_png.exists():
            meta["png_path"] = str(alt_png)
        else:
            meta["png_path"] = None

    return meta


def run_capture(profile_path: str) -> int:
    if not CAPTURE_SCRIPT.exists():
        print(f"ERROR: {CAPTURE_SCRIPT} not found", file=sys.stderr)
        return 1
    if not os.path.exists(profile_path):
        print(f"ERROR: profile not found: {profile_path}", file=sys.stderr)
        return 1

    env = os.environ.copy()
    env.setdefault("BOT_VISION_TMP", str(REPO_ROOT / "tmp" / "bot_vision"))
    env.setdefault("BOT_VISION_OUT", str(VISION_INBOX))

    cmd = ["node", str(CAPTURE_SCRIPT), "--profile", profile_path, "--once"]
    print(f"RUN: {' '.join(cmd)}")
    result = subprocess.run(cmd, env=env, cwd=str(HEADLESS_DIR), capture_output=True, text=True, timeout=120)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: capture failed (exit {result.returncode})", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    return result.returncode


def run_analysis(png_path: str, symbol: str, timeframe: str, telegram: bool, dry_run: bool) -> int:
    cmd = [
        sys.executable, str(ANALYZE_SCRIPT),
        "--png", png_path,
        "--symbol", symbol,
        "--timeframe", timeframe,
    ]
    if telegram:
        cmd.append("--telegram")
    if dry_run:
        cmd.append("--dry-run")

    print(f"RUN: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERROR: analysis failed (exit {result.returncode})", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    return result.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the vision pipeline: capture → analyze → output")
    ap.add_argument("--profile", default=str(HEADLESS_DIR / "profiles.btcusdt_poc.json"),
                    help="Playwright profile JSON")
    ap.add_argument("--once", action="store_true", default=True,
                    help="Run single capture cycle (default)")
    ap.add_argument("--telegram", action="store_true", help="Send Telegram notification")
    ap.add_argument("--dry-run", action="store_true", help="Skip OpenAI, produce stub analysis")
    ap.add_argument("--skip-capture", action="store_true", help="Skip capture, analyze latest in inbox")
    args = ap.parse_args()

    t0 = time.time()

    if not args.skip_capture:
        ret = run_capture(args.profile)
        if ret != 0:
            return ret

    meta = find_latest_capture(VISION_INBOX)
    if meta is None:
        print("ERROR: no capture found in inbox", file=sys.stderr)
        return 1

    status = meta.get("status", "")
    if status != "ready":
        print(f"SKIP: capture status is '{status}' — not ready for analysis", file=sys.stderr)
        return 1

    png_path = meta.get("png_path")
    if not png_path:
        print("ERROR: no PNG path in capture metadata", file=sys.stderr)
        return 1

    symbol = str(meta.get("symbol", "BTCUSDT"))
    timeframe = str(meta.get("timeframe", "15m"))

    print(f"\nAnalyzing: {symbol} {timeframe}")
    print(f"  PNG: {png_path}")
    print(f"  Capture ID: {meta.get('output_json', '?')}")

    ret = run_analysis(png_path, symbol, timeframe, telegram=args.telegram, dry_run=args.dry_run)
    if ret != 0:
        return ret

    elapsed = time.time() - t0
    print(f"\nPipeline complete in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
