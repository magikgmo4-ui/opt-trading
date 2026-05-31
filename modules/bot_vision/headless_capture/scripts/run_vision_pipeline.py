#!/usr/bin/env python3
"""
Pipeline orchestrator: Playwright capture → bot_vision_step2 analysis → DeskPro output.

Usage:
  python3 scripts/run_vision_pipeline.py --profile profiles.btcusdt_poc.json
  python3 scripts/run_vision_pipeline.py --profile profiles.btcusdt_poc.json --dry-run

This is a thin adapter. The heavy lifting (OpenAI vision, cropping, Telegram) is
done by bot_vision_step2 (modules/bot_vision_step2/). This script only:
  1. Runs capture_headless.js (Playwright) — bot_vision_step2 does not capture
  2. Delegates analysis to bot_vision_step2 analyze_latest
  3. Writes vision_analysis.v1 to the canonical DeskPro reader path

See also:
  modules/bot_vision_step2/          — operational analysis module
  modules/desk_snapshot_ingest/     — per-symbol snapshot ingestion
  scripts/desk_bridge/              — bridges vision → snapshot ingest
  modules/desk_pro/service/vision_analysis_reader.py  — DeskPro consumer
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
HEADLESS_DIR = REPO_ROOT / "modules" / "bot_vision" / "headless_capture"
CAPTURE_SCRIPT = HEADLESS_DIR / "capture_headless.js"
VISION_INBOX = Path(os.getenv("BOT_VISION_OUT", str(REPO_ROOT / "data" / "vision_inbox")))

DESKPRO_VISION_ANALYSIS_DIR = REPO_ROOT / "data" / "deskpro" / "inputs" / "vision_analysis"
DESKPRO_VISION_ANALYSIS_PATH = DESKPRO_VISION_ANALYSIS_DIR / "latest.json"

# bot_vision_step2 paths (production module, may not exist in dev env)
BOT_VISION_STEP2_APP = REPO_ROOT / "modules" / "bot_vision_step2" / "app" / "bot_vision_step2.py"
BOT_VISION_STEP2_VENV = Path("/opt/trading/.venvs/bot_vision_step2/bin/python")


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _capture_id(symbol: str, timeframe: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"cap_{ts}_{symbol}_{timeframe}"


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


def delegate_to_bot_vision_step2(meta: dict[str, Any]) -> int:
    """Delegate analysis to bot_vision_step2 analyze_latest (if available)."""
    if not BOT_VISION_STEP2_APP.exists():
        print("SKIP: bot_vision_step2 module not available in this environment", file=sys.stderr)
        return 2
    python = str(BOT_VISION_STEP2_VENV) if BOT_VISION_STEP2_VENV.exists() else "python3"
    env = os.environ.copy()
    # Point bot_vision_step2 to the capture output
    env.setdefault("VISION_INBOX", str(VISION_INBOX))
    env.setdefault("VISION_PROCESSED", str(VISION_INBOX))
    env.setdefault("DESKPRO_VISION_DIR", str(REPO_ROOT / "data" / "deskpro" / "vision"))
    env.setdefault("WORKDIR", str(REPO_ROOT / "tmp" / "bot_vision_step2"))
    cmd = [python, str(BOT_VISION_STEP2_APP), "analyze_latest"]
    print(f"RUN: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=180)
        if result.stdout:
            print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
        if result.returncode != 0:
            print(f"WARN: bot_vision_step2 exit {result.returncode}", file=sys.stderr)
            if result.stderr:
                print(result.stderr[-1000:], file=sys.stderr)
        return result.returncode
    except FileNotFoundError:
        print("SKIP: bot_vision_step2 not installed (venv missing)", file=sys.stderr)
        return 2
    except subprocess.TimeoutExpired:
        print("SKIP: bot_vision_step2 timed out", file=sys.stderr)
        return 2


def write_vision_analysis_stub(meta: dict[str, Any]) -> Path:
    """Write a vision_analysis.v1 stub pointing to the capture.

    The full analysis is produced by bot_vision_step2. This stub
    links the capture to the canonical DeskPro reader path.
    """
    symbol = str(meta.get("symbol", "BTCUSDT"))
    timeframe = str(meta.get("timeframe", "15m"))
    cid = _capture_id(symbol, timeframe)
    data = {
        "input_class": "vision_analysis.v1",
        "capture_id": cid,
        "symbol": symbol,
        "timeframe": timeframe,
        "analysis_ts": _utc_now_iso(),
        "source_module": "bot_vision_headless_capture",
        "freshness_state": "fresh",
        "capture_status": meta.get("status", "unknown"),
        "signals": [],
        "image_ref": meta.get("png_path") or "",
        "note": "Capture complete. Full analysis delegated to bot_vision_step2.",
    }
    DESKPRO_VISION_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DESKPRO_VISION_ANALYSIS_PATH.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, DESKPRO_VISION_ANALYSIS_PATH)
    print(f"OK: {DESKPRO_VISION_ANALYSIS_PATH}")
    return DESKPRO_VISION_ANALYSIS_PATH


def main() -> int:
    ap = argparse.ArgumentParser(description="Run vision pipeline: capture → bot_vision_step2 → DeskPro")
    ap.add_argument("--profile", default=str(HEADLESS_DIR / "profiles.btcusdt_poc.json"))
    ap.add_argument("--skip-capture", action="store_true", help="Skip capture, analyze latest in inbox")
    ap.add_argument("--dry-run", action="store_true", help="Skip bot_vision_step2, write stub only")
    ap.add_argument("--no-delegate", action="store_true", help="Skip bot_vision_step2 delegation")
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
    if meta.get("status") != "ready":
        print(f"SKIP: capture status is '{meta.get('status')}'", file=sys.stderr)
        return 1
    if not meta.get("png_path"):
        print("ERROR: no PNG path in capture metadata", file=sys.stderr)
        return 1

    symbol = str(meta.get("symbol", "BTCUSDT"))
    timeframe = str(meta.get("timeframe", "15m"))
    print(f"\nCapture ready: {symbol} {timeframe}")
    print(f"  PNG: {meta['png_path']}")

    write_vision_analysis_stub(meta)

    if not args.dry_run and not args.no_delegate:
        ret = delegate_to_bot_vision_step2(meta)
        if ret == 0:
            print("OK: bot_vision_step2 analysis complete")
        elif ret == 2:
            print("(non-bot_vision_step2 environment; stub written for manual analysis)")

    elapsed = time.time() - t0
    print(f"\nPipeline complete in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
