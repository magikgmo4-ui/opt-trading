from __future__ import annotations

"""SPCX score reader for DeskPro / Voice Operator.

Reads recent SPCX signal events from two sources:
  1. state/events_cdp.jsonl  -- CDP alerts (VWAP_RECLAIM, ORB_HIGH_BREAK, ...)
  2. state/events.jsonl       -- SPACEX_WIRE and other main webhook events

Adapts them to score_spcx() input format and returns the composite result.

Read-only. No side effects. No broker calls. monitor_only=True always.
"""

import json
from pathlib import Path
from typing import Any

from modules.data_center.spcx_composite_score import score_spcx
from modules.data_center.opening_session_metrics import compute_opening_metrics

# ---------------------------------------------------------------------------
# Default paths (relative to project root, resolved at import time)
# ---------------------------------------------------------------------------

_DEFAULT_CDP_JSONL = Path("state/events_cdp.jsonl")
_DEFAULT_EVENTS_JSONL = Path("state/events.jsonl")

_SYMBOL = "SPCX"

# ---------------------------------------------------------------------------
# CDP event name -> scorer event name aliases
# (CDP endpoint uses lowercase snake_case; scorer uses UPPER_SNAKE_CASE weights)
# ---------------------------------------------------------------------------

_CDP_ALIAS: dict[str, str] = {
    # ORB
    "ORB_BREAK_HIGH": "ORB_HIGH_BREAK",
    "ORB_BREAK_LOW": "ORB_LOW_BREAK",
    # Breakout levels -- TradingView sends event="breakout_high" for BREAK_174 and BREAK_180
    "BREAKOUT_HIGH": "BREAK_174",
    # Breakdown levels -- TradingView sends event="breakdown_low" for LOST_160 and TEST_148
    "BREAKDOWN_LOW": "BREAKDOWN",
    # Volume variants -> single scorer bucket
    "VOLUME_SPIKE": "VOLUME_SURGE",
    "RELATIVE_VOLUME_GT_2": "VOLUME_SURGE",
    "RELATIVE_VOLUME_GT_3": "VOLUME_SURGE",
    "VOLUME_ON_BREAKOUT": "VOLUME_SURGE",
    # VWAP state aliases
    "VWAP_LOSS": "VWAP_LOST",
    # Premarket (legacy alias for backward compat)
    "PREMARKET_HIGH_BREAK": "PREMARKET_HIGH_BREAK",
    "PREMARKET_GAP": "PREMARKET_HIGH_BREAK",    # legacy alias
    "PREMARKET_LOW_BREAK": "PREMARKET_LOW_BREAK",
    "PREMARKET_HIGH_REJECT": "PREMARKET_HIGH_REJECT",
    "PREMARKET_LOW_REJECT": "PREMARKET_LOW_REJECT",
    # Gap events
    "GAP_OPEN_UP": "GAP_OPEN_UP",
    "GAP_OPEN_DOWN": "GAP_OPEN_DOWN",
    "GAP_FILL_STARTED": "GAP_FILL_STARTED",
    "GAP_FILL_COMPLETED": "GAP_FILL_COMPLETED",
    # Opening exhaustion
    "OPENING_EXHAUSTION": "OPENING_EXHAUSTION",
}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _read_jsonl(path: Path, limit: int) -> list[dict]:
    """Read last `limit` JSON lines from a .jsonl file. Returns [] on any failure."""
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        out: list[dict] = []
        for line in lines[-limit:]:
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
                if isinstance(parsed, dict):
                    out.append(parsed)
            except json.JSONDecodeError:
                continue
        return out
    except Exception:
        return []


def _adapt_cdp_events(raw: list[dict]) -> list[dict]:
    """Filter CDP events to SPCX and normalize to scorer input format.

    CDP events stored in events_cdp.jsonl have the shape:
        {_schema, source, symbol, timeframe, event, price, volume, flags, _ts}

    Optional enrichment fields (vwap, orb_high, bias) are in `flags` if the
    TradingView alert included them.
    """
    out: list[dict] = []
    for e in raw:
        # Only process signal_event.v1 CDP rows (or untagged rows from this file)
        schema = e.get("_schema", "")
        if schema and schema != "signal_event.v1":
            continue
        if str(e.get("symbol", "")).upper() != _SYMBOL:
            continue

        raw_event = str(e.get("event", "")).upper()
        if not raw_event:
            continue

        # Apply alias mapping
        scorer_event = _CDP_ALIAS.get(raw_event, raw_event)

        # Pull enrichment from flags dict if present
        flags: dict = e.get("flags") or {}
        adapted: dict[str, Any] = {
            "symbol": _SYMBOL,
            "event": scorer_event,
            "price": e.get("price"),
            "vwap": flags.get("vwap"),
            "orb_high": flags.get("orb_high"),
            "orb_low": flags.get("orb_low"),
            "bias": flags.get("bias"),
            "timeframe": e.get("timeframe"),
            "source": "cdp",
        }
        out.append(adapted)
    return out


def _adapt_wire_events(raw: list[dict]) -> list[dict]:
    """Extract SPACEX_WIRE signals from main events.jsonl.

    Main webhook events have the shape:
        {engine, signal, symbol, tf, price, tp, sl, reason, _ts, ...}

    SPACEX_WIRE arrives here as signal="SPACEX_WIRE".
    """
    out: list[dict] = []
    for e in raw:
        if str(e.get("symbol", "")).upper() != _SYMBOL:
            continue
        signal = str(e.get("signal", "")).upper()
        if signal == "SPACEX_WIRE":
            out.append({
                "symbol": _SYMBOL,
                "event": "SPACEX_WIRE",
                "price": e.get("price"),
                "timeframe": e.get("tf"),
                "source": "webhook",
            })
    return out


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def read_spcx_score(
    cdp_path: Path | str | None = None,
    events_path: Path | str | None = None,
    limit: int = 50,
) -> dict[str, Any]:
    """Read recent SPCX signals and return a composite score dict.

    Aggregates CDP alerts and SPACEX_WIRE events, adapts them to score_spcx()
    input format, and returns the full score result.

    Args:
        cdp_path:    Path to events_cdp.jsonl. Defaults to state/events_cdp.jsonl.
        events_path: Path to events.jsonl. Defaults to state/events.jsonl.
        limit:       Max lines to read from each file (tail).

    Returns:
        score_spcx() result dict enriched with a "data_source" metadata block.
        Always includes monitor_only=True.
        Returns a zero-score result (grade=C, setup_state=watch) when no events
        are found -- never raises.
    """
    cdp_path = Path(cdp_path) if cdp_path is not None else _DEFAULT_CDP_JSONL
    events_path = Path(events_path) if events_path is not None else _DEFAULT_EVENTS_JSONL

    raw_cdp = _read_jsonl(cdp_path, limit)
    raw_events = _read_jsonl(events_path, limit)

    adapted_cdp = _adapt_cdp_events(raw_cdp)
    adapted_wire = _adapt_wire_events(raw_events)

    all_events = adapted_cdp + adapted_wire

    # Compute opening session metrics (Phase 2)
    opening_metrics = compute_opening_metrics(all_events)

    result = score_spcx(all_events, opening_metrics=opening_metrics)
    result["data_source"] = {
        "cdp_events": len(adapted_cdp),
        "wire_events": len(adapted_wire),
        "total_input_events": len(all_events),
    }
    return result
