#!/usr/bin/env python3
"""
schedule_orchestrator — Central scheduler for bot_vision headless captures.

Reads:
  - capture_map.json       → target assets + screens
  - trigger_config.json    → schedules, market hours, cooldowns
  - screen_types.json      → analyzer dispatch per screen type

Decides:
  Which profiles to run NOW based on:
    - Schedule interval (every_15m, every_1h, etc.)
    - Market hours (US market 09:30-16:00 ET, crypto 24/7)
    - Cooldown after failure
    - Consecutive failure cap

Dispatches:
  - CHART_TECHNICAL / ETF_CRYPTO → capture_headless.js → bot_vision_step2 → vision_analysis_writer → telegram_filter
  - DASHBOARD_MACRO → capture_headless.js → compose_quad → bot_vision_step2 → vision_analysis_writer
  - LIQUIDITY_COINGLASS / FUNDING_* / OI_* / LS_RATIO_* → capture_headless.js → coinglass_ocr_analyzer → vision_context_writer
  - SCREENER_STOCKS → capture_headless.js → screener_analyzer → screener_writer

Usage:
  python3 scripts/schedule_orchestrator.py --dry-run          # preview what would run
  python3 scripts/schedule_orchestrator.py                    # run due captures
  python3 scripts/schedule_orchestrator.py --force-all        # run everything
  python3 scripts/schedule_orchestrator.py --once --profile profiles.production.json  # one-shot (legacy compat)
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

CAPTURE_MAP_PATH = HEADLESS_DIR / "capture_map.json"
SCREEN_TYPES_PATH = HEADLESS_DIR / "screen_types.json"
TRIGGER_CONFIG_PATH = HEADLESS_DIR / "trigger_config.json"
STATE_DIR = REPO_ROOT / "data" / "bot_vision" / "orchestrator_state"
STATE_PATH = STATE_DIR / "state.json"
COOLDOWN_PATH = STATE_DIR / "cooldown.json"

CAPTURE_SCRIPT = HEADLESS_DIR / "capture_headless.js"
VISION_PIPELINE = HEADLESS_DIR / "scripts" / "run_vision_pipeline.py"


# ── Schedule resolution ───────────────────────────────────

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_or_init(path: Path) -> dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def _save_state(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


# ── Profile loading ───────────────────────────────────────

def _load_all_profiles() -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for fname in ["profiles.production.json", "profiles.coinglass.json",
                   "profiles.macro_dashboard.json", "profiles.supplementary.json"]:
        path = HEADLESS_DIR / fname
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    profiles.extend(data)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
    return profiles


# ── Schedule check ────────────────────────────────────────

def _interval_to_profile_key(interval_seconds: int) -> str:
    if interval_seconds <= 900:
        return "every_15m"
    elif interval_seconds <= 3600:
        return "every_1h"
    elif interval_seconds <= 14400:
        return "every_4h"
    elif interval_seconds <= 21600:
        return "every_6h"
    else:
        return "every_24h"


def _schedule_key_for_profile(profile: dict[str, Any], trigger_config: dict[str, Any]) -> str:
    symbol = str(profile.get("symbol", ""))
    screen_type = str(profile.get("screen_type", "CHART_TECHNICAL"))

    # 1. Check asset override
    for override in trigger_config.get("asset_overrides", []):
        if override.get("symbol") == symbol:
            return override.get("schedule", "every_1h")

    # 2. Check screen_type default
    defaults = trigger_config.get("screen_type_defaults", {})
    st_default = defaults.get(screen_type, {})
    return st_default.get("schedule", "every_1h")


def _is_due(profile: dict[str, Any], state: dict[str, Any], trigger_config: dict[str, Any]) -> bool:
    now = _utc_now()
    now_ts = now.timestamp()

    key = profile.get("page_id", profile.get("symbol", "unknown"))
    last_run = state.get(key, {}).get("last_run_ts", 0)

    sched_key = _schedule_key_for_profile(profile, trigger_config)
    sched = trigger_config.get("schedules", {}).get(sched_key, {})
    interval = sched.get("interval_seconds", 3600)
    jitter = sched.get("max_jitter_seconds", 120)

    elapsed = now_ts - last_run
    return elapsed >= (interval - jitter)


def _check_market_hours(profile: dict[str, Any], trigger_config: dict[str, Any]) -> bool:
    symbol = str(profile.get("symbol", ""))
    global_cfg = trigger_config.get("global", {})

    if not global_cfg.get("market_hours_enabled", True):
        return True

    cfg_path = HEADLESS_DIR / "capture_headless.js"
    if cfg_path.exists():
        source = cfg_path.read_text(encoding="utf-8")
        if "BOT_VISION_MARKET_HOURS" in source:
            prelude = source[:source.index("const VALID_WAIT_UNTIL")]
            prelude = prelude.replace("#!/usr/bin/env node\n", "", 1)
            prelude = prelude.replace("const { chromium } = require('playwright');", "")
            env = os.environ.copy()
            env.setdefault("BOT_VISION_MARKET_HOURS", "1")
            result = subprocess.run(
                ["node", "-e", """
                    const mh = %s;
                    const symbol = %s;
                    %s
                    console.log(isInMarketHours(symbol) ? 'PASS' : 'BLOCKED');
                """ % (
                    json.dumps({}),
                    json.dumps(symbol),
                    prelude,
                )],
                capture_output=True, text=True, timeout=10, cwd=str(HEADLESS_DIR),
            )
            return "PASS" in result.stdout
    return True


# ── Runner dispatch ───────────────────────────────────────

def _run_capture(profile: dict[str, Any], dry_run: bool = False) -> int:
    screen_type = str(profile.get("screen_type", "CHART_TECHNICAL"))
    symbol = str(profile.get("symbol", "unknown"))
    page_id = str(profile.get("page_id", symbol))

    print(f"  [{screen_type}] {symbol} ({page_id})")

    if dry_run:
        return 0

    env = os.environ.copy()
    env.setdefault("BOT_VISION_TMP", str(REPO_ROOT / "tmp" / "bot_vision"))
    env.setdefault("BOT_VISION_OUT", str(REPO_ROOT / "data" / "vision_inbox"))

    result = subprocess.run(
        ["node", str(CAPTURE_SCRIPT), "--profile", "/dev/stdin", "--once"],
        input=json.dumps(profile),
        capture_output=True, text=True, timeout=120, env=env,
    )

    if result.returncode != 0:
        print(f"    FAIL capture (exit {result.returncode})")
        if result.stderr:
            print(f"    {result.stderr.strip()[:200]}")
        return result.returncode

    print(f"    OK capture")
    return 0


def _run_analysis(screen_type: str, dry_run: bool = False) -> int:
    if dry_run:
        return 0

    pipeline_args = [sys.executable or "python3", str(VISION_PIPELINE), "--skip-capture"]

    if screen_type in {"LIQUIDITY_COINGLASS", "FUNDING_COINGLASS", "OI_COINGLASS", "LS_RATIO_COINGLASS"}:
        pass  # pipeline handles Coinglass dispatch

    if screen_type == "SCREENER_STOCKS":
        pass  # pipeline handles Screener dispatch

    result = subprocess.run(pipeline_args, capture_output=True, text=True, timeout=300)
    if result.stdout:
        last_line = [l for l in result.stdout.strip().split("\n") if l.strip()][-1]
        print(f"    {last_line}")
    return result.returncode


# ── Main orchestrator ─────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description="bot_vision schedule orchestrator")
    ap.add_argument("--dry-run", action="store_true", help="Preview what would run")
    ap.add_argument("--force-all", action="store_true", help="Run all profiles regardless of schedule")
    ap.add_argument("--once", action="store_true", help="One-shot mode with --profile")
    ap.add_argument("--profile", default=None, help="Specific profile file (one-shot mode)")
    ap.add_argument("--reset-state", action="store_true", help="Reset all state/cooldown")
    args = ap.parse_args()

    # Load configs
    try:
        capture_map = _load_json(CAPTURE_MAP_PATH)
        screen_types = _load_json(SCREEN_TYPES_PATH)
        trigger_config = _load_json(TRIGGER_CONFIG_PATH)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: config load failed: {e}", file=sys.stderr)
        return 1

    if args.reset_state:
        for p in [STATE_PATH, COOLDOWN_PATH]:
            if p.exists():
                p.unlink()
        print("OK: state reset")
        return 0

    state = _load_or_init(STATE_PATH)
    cooldown = _load_or_init(COOLDOWN_PATH)
    now = _utc_now()
    now_ts = now.timestamp()

    profiles: list[dict[str, Any]] = []

    if args.once and args.profile:
        path = Path(args.profile)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            profiles = data if isinstance(data, list) else [data]
        else:
            print(f"ERROR: profile not found: {path}", file=sys.stderr)
            return 1
    else:
        profiles = _load_all_profiles()

    total = len(profiles)
    ran = 0
    skipped_schedule = 0
    skipped_cooldown = 0
    skipped_market_hours = 0
    failed = 0

    print(f"bot_vision orchestrator — {_utc_now().isoformat()}")
    print(f"Profiles loaded: {total}")
    if args.dry_run:
        print("DRY RUN — no captures will execute")
    print()

    for profile in profiles:
        key = profile.get("page_id", profile.get("symbol", "unknown"))
        screen_type = str(profile.get("screen_type", "CHART_TECHNICAL"))
        symbol = str(profile.get("symbol", "unknown"))

        # Check cooldown
        prof_cooldown = cooldown.get(key, 0)
        if prof_cooldown > now_ts:
            remaining = int(prof_cooldown - now_ts)
            print(f"  SKIP {symbol} ({key}) — cooldown {remaining}s remaining")
            skipped_cooldown += 1
            continue

        # Check schedule
        if not args.force_all and not args.once:
            if not _is_due(profile, state, trigger_config):
                skipped_schedule += 1
                continue

        # Check market hours (skip if force-all or once)
        if not args.force_all and not args.once:
            if not _check_market_hours(profile, trigger_config):
                print(f"  SKIP {symbol} ({key}) — outside market hours")
                skipped_market_hours += 1
                continue

        # Run capture
        ret = _run_capture(profile, dry_run=args.dry_run)

        if ret != 0:
            failed += 1
            if args.dry_run:
                continue
            consecutive = state.get(key, {}).get("consecutive_failures", 0) + 1
            max_fail = trigger_config.get("global", {}).get("max_consecutive_failures", 3)
            if consecutive >= max_fail:
                cool_min = trigger_config.get("global", {}).get("cooldown_after_failure_minutes", 15)
                cooldown[key] = now_ts + cool_min * 60
                print(f"    -> cooldown {cool_min}min (after {consecutive} failures)")
            state[key] = {"last_run_ts": now_ts, "consecutive_failures": consecutive, "last_status": "failed"}
        else:
            ran += 1
            if args.dry_run:
                continue
            state[key] = {"last_run_ts": now_ts, "consecutive_failures": 0, "last_status": "ok"}

        # Run analysis pipeline after successful capture (only in non-dry-run non-once mode)
        if ret == 0 and not args.dry_run and not args.once:
            _run_analysis(screen_type, dry_run=args.dry_run)

        _save_state(STATE_PATH, state)
        _save_state(COOLDOWN_PATH, cooldown)

    print(f"\nSummary: {ran} ran, {failed} failed, {skipped_schedule} skipped (schedule), {skipped_cooldown} skipped (cooldown), {skipped_market_hours} skipped (market hours)")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
