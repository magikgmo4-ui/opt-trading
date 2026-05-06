"""
signal_event_adapter.py — Minimal V0 → V1 adapter for signal_event.

Converts webhook runtime events (V0: signal, tf, _ts) into the canonical
signal_event V1 format (direction, timeframe, timestamp, status, etc.).

This adapter is read-only / stateless. It does NOT modify events.jsonl,
does NOT call webhook, does NOT send Telegram.

Usage:
    from modules.desk_pro.signal_event_adapter import (
        normalize_signal_event_v1,
        validate_signal_event_v1,
        read_events_v1,
        payload_hash,
    )
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── V0 → V1 field mapping ──────────────────────────────────────────
_V0_TO_V1_MAP = {
    "engine": "engine",
    "symbol": "symbol",
    "tf": "timeframe",
    "signal": "direction",
    "_ts": "timestamp",
}

_RENAME_MAP = {
    "tf": "timeframe",
    "signal": "direction",
    "_ts": "timestamp",
}

# ── Constants ──────────────────────────────────────────────────────
_SOURCE = "tradingview.webhook"
_EVENT_TYPE = "signal_event"
_STATUS_ACCEPTED = "accepted"
_VALID_DIRECTIONS = {"BUY", "SELL"}
_VALID_STATUSES = {"accepted", "rejected", "skipped", "error"}


def _safe_str(v: Any) -> str:
    if v is None:
        return ""
    return str(v).strip()


def _safe_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _parse_iso(ts: str) -> Optional[datetime]:
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def payload_hash(payload: dict) -> str:
    """Compute a deterministic SHA-256 hash of the raw V0 payload."""
    canonical = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def normalize_signal_event_v1(v0_payload: dict) -> dict:
    """
    Convert a V0 webhook event dict into a V1 signal_event dict.

    Input (V0 — from events.jsonl):
        {engine, signal, symbol, tf, price, tp, sl, reason, _ts, _ip,
         qty, risk_usd, risk_real_usd, key, ...}

    Output (V1 — canonical):
        {source, event_type, engine, symbol, timeframe, direction,
         timestamp, status, payload_hash, raw_payload_ref, meta,
         risk_context, visual_context_ref, desk_snapshot_ref, errors}
    """
    if not isinstance(v0_payload, dict):
        return _error_event(["payload is not a dict"])

    errors: List[str] = []

    # ── Required: engine ──
    engine = _safe_str(v0_payload.get("engine"))
    if not engine:
        errors.append("missing engine")

    # ── Required: symbol ──
    symbol = _safe_str(v0_payload.get("symbol"))
    if not symbol:
        errors.append("missing symbol")

    # ── Required: direction (V0: signal) ──
    direction = _safe_str(v0_payload.get("signal")).upper()
    if direction not in _VALID_DIRECTIONS:
        errors.append(f"invalid direction: {direction!r}")

    # ── Required: timeframe (V0: tf) ──
    timeframe = _safe_str(v0_payload.get("tf"))
    if not timeframe:
        errors.append("missing timeframe")

    # ── Required: timestamp (V0: _ts) ──
    raw_ts = _safe_str(v0_payload.get("_ts"))
    timestamp = raw_ts  # pass through; validate in validate_signal_event_v1

    # ── Optional: meta ──
    meta: Dict[str, Any] = {}
    for k in ("price", "tp", "sl", "reason"):
        v = v0_payload.get(k)
        if v is not None:
            meta[k] = v
    # _ip goes to meta.debug
    ip = v0_payload.get("_ip")
    if ip:
        meta.setdefault("debug", {})["client_ip"] = ip

    # ── Optional: risk_context ──
    risk_context: Dict[str, Any] = {}
    for k in ("qty", "risk_usd", "risk_real_usd"):
        v = v0_payload.get(k)
        if v is not None:
            risk_context[k] = v

    # ── Optional: payload_hash ──
    phash = payload_hash(v0_payload)

    # ── Build V1 event ──
    v1: Dict[str, Any] = {
        "source": _SOURCE,
        "event_type": _EVENT_TYPE,
        "engine": engine,
        "symbol": symbol,
        "timeframe": timeframe,
        "direction": direction,
        "timestamp": timestamp,
        "status": _STATUS_ACCEPTED,
        "payload_hash": phash,
        "raw_payload_ref": None,
        "meta": meta if meta else None,
        "risk_context": risk_context if risk_context else None,
        "visual_context_ref": None,
        "desk_snapshot_ref": None,
        "errors": errors,
    }

    return v1


def _error_event(errors: List[str]) -> dict:
    """Return a minimal V1 event with status=error."""
    return {
        "source": _SOURCE,
        "event_type": _EVENT_TYPE,
        "engine": "",
        "symbol": "",
        "timeframe": "",
        "direction": "",
        "timestamp": "",
        "status": "error",
        "payload_hash": None,
        "raw_payload_ref": None,
        "meta": None,
        "risk_context": None,
        "visual_context_ref": None,
        "desk_snapshot_ref": None,
        "errors": errors,
    }


def validate_signal_event_v1(event: dict) -> Tuple[bool, List[str]]:
    """
    Validate a V1 signal_event dict.

    Returns:
        (is_valid, list_of_errors)

    Blocking errors (is_valid=False):
        - missing engine
        - missing symbol
        - missing timeframe
        - invalid direction
        - missing or unparseable timestamp

    Non-blocking warnings (is_valid=True, returned in list):
        - missing optional fields
        - status != accepted
    """
    if not isinstance(event, dict):
        return False, ["event is not a dict"]

    errors: List[str] = []
    blocking = False

    # Required fields
    if not _safe_str(event.get("engine")):
        errors.append("missing engine")
        blocking = True

    if not _safe_str(event.get("symbol")):
        errors.append("missing symbol")
        blocking = True

    if not _safe_str(event.get("timeframe")):
        errors.append("missing timeframe")
        blocking = True

    direction = _safe_str(event.get("direction")).upper()
    if direction not in _VALID_DIRECTIONS:
        errors.append(f"invalid direction: {direction!r}")
        blocking = True

    # Timestamp validation
    ts = _safe_str(event.get("timestamp"))
    if not ts:
        errors.append("missing timestamp")
        blocking = True
    elif _parse_iso(ts) is None:
        errors.append(f"unparseable timestamp: {ts!r}")
        blocking = True

    # Status (non-blocking)
    status = _safe_str(event.get("status"))
    if status and status not in _VALID_STATUSES:
        errors.append(f"unknown status: {status!r}")

    # Source/event_type (non-blocking, derived)
    if _safe_str(event.get("source")) != _SOURCE:
        errors.append(f"unexpected source: {event.get('source')!r}")

    if _safe_str(event.get("event_type")) != _EVENT_TYPE:
        errors.append(f"unexpected event_type: {event.get('event_type')!r}")

    return not blocking, errors


def read_events_v1(
    events_jsonl: str | Path = "/opt/trading/state/events.jsonl",
    limit: int = 50,
    only_accepted: bool = True,
) -> List[dict]:
    """
    Read V0 events from events.jsonl, normalize to V1, and return.

    Args:
        events_jsonl: path to the V0 events file
        limit: max events to read (from end)
        only_accepted: if True, skip events that fail validation

    Returns:
        list of V1 signal_event dicts
    """
    path = Path(events_jsonl)
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    out: List[dict] = []

    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            v0 = json.loads(line)
        except json.JSONDecodeError:
            continue

        v1 = normalize_signal_event_v1(v0)

        if only_accepted:
            is_valid, _ = validate_signal_event_v1(v1)
            if not is_valid:
                continue

        out.append(v1)

    return out
