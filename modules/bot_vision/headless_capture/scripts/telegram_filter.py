#!/usr/bin/env python3
"""
telegram_filter — filters bot_vision_step2 analysis output for Telegram dispatch.

Rules:
  - Only dispatch if at least one signal has confidence >= CONFIDENCE_THRESHOLD
  - Generate a concise filtered summary (not the full analysis text)
  - Throttle: skip signals matching recent sends within COOLDOWN_MINUTES
  - Supports --dry-run to preview without sending

Usage:
  python3 scripts/telegram_filter.py                              # analyze latest run
  python3 scripts/telegram_filter.py --run-dir <path>             # specific run
  python3 scripts/telegram_filter.py --stdin                      # read summary.json from stdin
  python3 scripts/telegram_filter.py --dry-run                    # preview only
  python3 scripts/telegram_filter.py --confidence 0.80            # custom threshold
  python3 scripts/telegram_filter.py --cooldown-minutes 60        # throttle cooldown

Integration:
  Called by run_vision_pipeline.py after bot_vision_step2 analysis.
  Outputs JSON to stdout with {send, summary, signals, reason} for the caller
  to dispatch via Telegram if send=true.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
RUN_DIR_DEFAULT = REPO_ROOT / "data" / "deskpro" / "vision" / "latest"
COOLDOWN_STATE_DIR = REPO_ROOT / "data" / "bot_vision" / "telegram_cooldown"
COOLDOWN_STATE_PATH = COOLDOWN_STATE_DIR / "cooldown_state.json"

CONFIDENCE_THRESHOLD = 0.70
MAX_SUMMARY_LENGTH = 3500
DEFAULT_COOLDOWN_MINUTES = 30


def read_summary(source: Path | None = None) -> dict[str, Any] | None:
    if source is None:
        latest_link = REPO_ROOT / "data" / "deskpro" / "vision" / "latest"
        if latest_link.exists():
            source = latest_link.resolve() / "summary.json"
        else:
            source = RUN_DIR_DEFAULT / "summary.json"

    if not source.exists():
        return None
    try:
        return json.loads(source.read_text(encoding="utf-8"))
    except Exception:
        return None


def _signal_hash(sig: dict[str, Any]) -> str:
    t = str(sig.get("type", ""))
    v = str(sig.get("value", ""))
    s = str(sig.get("symbol", ""))
    raw = f"{t}:{v}:{s}"
    return hashlib.md5(raw.encode()).hexdigest()


def _load_cooldown_state() -> dict[str, float]:
    if COOLDOWN_STATE_PATH.exists():
        try:
            return json.loads(COOLDOWN_STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_cooldown_state(state: dict[str, float]) -> None:
    COOLDOWN_STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = COOLDOWN_STATE_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, COOLDOWN_STATE_PATH)


def _filter_throttled(
    signals: list[dict[str, Any]],
    state: dict[str, float],
    cooldown_seconds: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    now = time.time()
    allowed: list[dict[str, Any]] = []
    skipped_reasons: list[str] = []
    for sig in signals:
        h = _signal_hash(sig)
        last_sent = state.get(h, 0)
        if now - last_sent < cooldown_seconds:
            remaining = int(cooldown_seconds - (now - last_sent))
            skipped_reasons.append(
                f"{sig.get('type', '?')}={sig.get('value', '?')} "
                f"(cooldown {remaining}s remaining)"
            )
        else:
            allowed.append(sig)
    return allowed, skipped_reasons


def _confidence(val: Any) -> float:
    if isinstance(val, (int, float)):
        return float(val)
    return 0.0


def filter_signals(
    summary: dict[str, Any],
    min_confidence: float = CONFIDENCE_THRESHOLD,
) -> list[dict[str, Any]]:
    signals_raw = summary.get("signals", {})
    if isinstance(signals_raw, dict):
        charts = signals_raw.get("charts", [])
        if charts:
            return charts
        return []
    if isinstance(signals_raw, list):
        return [s for s in signals_raw if _confidence(s.get("confidence", 0)) >= min_confidence]
    return []


def build_telegram_summary(
    summary: dict[str, Any],
    filtered_signals: list[dict[str, Any]],
    min_confidence: float,
    throttled_reasons: list[str] | None = None,
) -> dict[str, Any]:
    text = summary.get("analysis_text", "")
    lines = text.split("\n") if text else []
    condensed = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(line.lower().startswith(kw) for kw in ["a)", "b)", "c)", "d)", "e)", "f)", "-"]):
            # Keep structured bullet points
            condensed.append(line)
        elif any(kw in line.lower() for kw in ["support", "résistance", "tendance", "signal", "invalidation", "objectif", "target", "bias", "structure"]):
            condensed.append(line)

    summary_text = "\n".join(condensed[:20])
    if not summary_text:
        summary_text = text[:500] if text else "No analysis available"

    if len(summary_text) > MAX_SUMMARY_LENGTH:
        summary_text = summary_text[: MAX_SUMMARY_LENGTH - 20] + "\n…(truncated)"

    throttled_count = len(throttled_reasons) if throttled_reasons else 0
    should_send = len(filtered_signals) > 0

    reasons = []
    if should_send:
        reasons.append(f"{len(filtered_signals)} signal(s) above {min_confidence:.0%} confidence")
    else:
        reasons.append("No signals above confidence threshold")
    if throttled_count > 0:
        reasons.append(f"{throttled_count} signal(s) throttled (cooldown)")

    return {
        "send": should_send,
        "reason": "; ".join(reasons),
        "min_confidence": min_confidence,
        "throttled_count": throttled_count,
        "throttled_signals": throttled_reasons or [],
        "run_id": summary.get("run_id", ""),
        "symbols": list({s.get("symbol", s.get("bias", "unknown")) for s in filtered_signals}) if filtered_signals else [],
        "filtered_signal_count": len(filtered_signals),
        "summary": summary_text,
        "signals": filtered_signals,
        "telegram_payload": {
            "message": summary_text,
            "disable_web_page_preview": True,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Filter bot_vision_step2 analysis for Telegram dispatch")
    ap.add_argument("--run-dir", default=None, help="Path to bot_vision_step2 run directory")
    ap.add_argument("--stdin", action="store_true", help="Read summary.json from stdin")
    ap.add_argument("--dry-run", action="store_true", help="Preview filter decision without output")
    ap.add_argument("--confidence", type=float, default=CONFIDENCE_THRESHOLD, help=f"Minimum confidence threshold (default: {CONFIDENCE_THRESHOLD})")
    ap.add_argument("--cooldown-minutes", type=int, default=DEFAULT_COOLDOWN_MINUTES, help=f"Throttle cooldown in minutes (default: {DEFAULT_COOLDOWN_MINUTES}, 0=disabled)")
    ap.add_argument("--no-throttle", action="store_true", help="Disable throttling")
    args = ap.parse_args()

    summary = None
    if args.stdin:
        try:
            summary = json.loads(sys.stdin.read())
        except json.JSONDecodeError as e:
            print(f"ERROR: invalid JSON from stdin: {e}", file=sys.stderr)
            return 1
    elif args.run_dir:
        summary = read_summary(Path(args.run_dir) / "summary.json")
    else:
        summary = read_summary()

    if summary is None:
        print("ERROR: no summary.json found", file=sys.stderr)
        return 1

    filtered = filter_signals(summary, args.confidence)

    throttled_reasons: list[str] = []
    cooldown_state = {}
    cooldown_seconds = args.cooldown_minutes * 60

    if not args.no_throttle and cooldown_seconds > 0:
        cooldown_state = _load_cooldown_state()
        filtered, throttled_reasons = _filter_throttled(filtered, cooldown_state, cooldown_seconds)

    result = build_telegram_summary(summary, filtered, args.confidence, throttled_reasons)

    if args.dry_run:
        status = "WOULD_SEND" if result["send"] else "WOULD_SKIP"
        print(f"[{status}] {result['reason']}")
        if result["send"]:
            print(f"  Signals: {result['filtered_signal_count']}")
            print(f"  Summary preview: {result['summary'][:200]}...")
        if throttled_reasons:
            print(f"  Throttled: {len(throttled_reasons)} signal(s)")
            for r in throttled_reasons[:3]:
                print(f"    - {r}")
        return 0

    # Update cooldown state for sent signals
    if result["send"] and not args.no_throttle and cooldown_seconds > 0:
        now = time.time()
        for sig in filtered:
            h = _signal_hash(sig)
            cooldown_state[h] = now
        _save_cooldown_state(cooldown_state)

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0 if result["send"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
