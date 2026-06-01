#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[4]
DESKPRO_TELEGRAM_DIR = REPO_ROOT / "data" / "deskpro" / "inputs" / "telegram_claim"
DESKPRO_TELEGRAM_PATH = DESKPRO_TELEGRAM_DIR / "latest.json"


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _claim_type(screen_type: str) -> str:
    if screen_type == "NEWS_SENTIMENT":
        return "news_alert"
    if screen_type == "SCREENER_STOCKS":
        return "alpha_signal"
    return "trade_context"


def _direction_from_signals(signals: list[dict[str, Any]]) -> str | None:
    for signal in signals:
        if signal.get("type") == "trend_direction":
            value = str(signal.get("value", "")).lower()
            if value in {"bullish", "haussier", "long"}:
                return "long"
            if value in {"bearish", "baissier", "short"}:
                return "short"
    return None


def _levels_from_signals(signals: list[dict[str, Any]]) -> list[float]:
    levels: list[float] = []
    for signal in signals:
        value = signal.get("value")
        if isinstance(value, (int, float)):
            levels.append(float(value))
        elif isinstance(value, str) and re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value):
            levels.append(float(value))
    deduped = []
    seen = set()
    for level in levels:
        if level not in seen:
            seen.add(level)
            deduped.append(level)
    return deduped


def build_claim(
    telegram_result: dict[str, Any],
    *,
    screen_type: str,
    symbol: str,
    timeframe: str,
    source: str = "bot_vision",
    channel_id: str | None = None,
    message_id: str | None = None,
) -> dict[str, Any]:
    run_id = str(telegram_result.get("run_id", "run"))
    signals = telegram_result.get("signals", [])
    if not isinstance(signals, list):
        signals = []
    confidences = [float(s.get("confidence", 0.0)) for s in signals if isinstance(s.get("confidence"), (int, float))]
    confidence = max(confidences) if confidences else 0.0
    channel = channel_id or os.getenv("TELEGRAM_CHAT_ID") or ""
    msg_id = message_id or str(uuid.uuid4())[:8]

    entities: dict[str, Any] = {
        "levels": _levels_from_signals(signals),
        "confidence": round(confidence, 3),
        "screen_type": screen_type,
        "signal_count": len(signals),
        "summary": telegram_result.get("summary", ""),
    }
    direction = _direction_from_signals(signals)
    if direction:
        entities["direction"] = direction

    claim_ts = _utc_now_iso()
    claim_id = f"tg_claim_{claim_ts[:19].replace(':', '').replace('-', '')}_{symbol or 'UNKNOWN'}"

    return {
        "input_class": "telegram_claim.v1",
        "claim_id": claim_id,
        "source": source,
        "channel_id": channel,
        "message_id": msg_id,
        "symbol": symbol,
        "timeframe": timeframe,
        "claim_ts": claim_ts,
        "claim_type": _claim_type(screen_type),
        "text": telegram_result.get("summary", ""),
        "entities": entities,
        "refs": {
            "telegram_message_ref": f"telegram://{channel}/{msg_id}" if channel else "telegram://unknown/unknown",
            "run_id": run_id,
        },
    }


def write_claim(data: dict[str, Any]) -> Path:
    DESKPRO_TELEGRAM_DIR.mkdir(parents=True, exist_ok=True)
    tmp = DESKPRO_TELEGRAM_PATH.with_suffix(".json.uploading")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, DESKPRO_TELEGRAM_PATH)
    return DESKPRO_TELEGRAM_PATH


def main() -> int:
    ap = argparse.ArgumentParser(description="Write canonical telegram_claim.v1 from bot-vision Telegram output")
    ap.add_argument("--stdin", action="store_true", help="Read telegram result JSON from stdin")
    ap.add_argument("--screen-type", required=True)
    ap.add_argument("--symbol", required=True)
    ap.add_argument("--timeframe", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.stdin:
        raise SystemExit("ERROR: --stdin required")
    payload = json.loads(sys.stdin.read())
    claim = build_claim(payload, screen_type=args.screen_type, symbol=args.symbol, timeframe=args.timeframe)
    if args.dry_run:
        print(json.dumps(claim, indent=2, ensure_ascii=False))
        return 0
    path = write_claim(claim)
    print(f"OK: DeskPro <- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
