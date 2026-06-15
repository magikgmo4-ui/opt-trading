"""Data Center writer for signal_event.v1 — CDP TradingView events sink.

Writes per-symbol rolling window and global latest to:
  data/data_center/views/signal_event.v1/latest.json
  data/data_center/views/signal_event.v1/by_symbol/<SYMBOL>/latest.json
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SIGNAL_DIR = PROJECT_ROOT / "data" / "data_center" / "views" / "signal_event.v1"
MAX_EVENTS = 50


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_signal_event(payload: dict[str, Any]) -> dict[str, Any]:
    """Write a signal_event.v1 payload to Data Center views.

    Args:
        payload: Normalized signal_event.v1 dict from cdp_normalizer.

    Returns:
        {"ok": True, "symbol": "...", "total_events": N, ...}
    """
    symbol = (payload.get("symbol") or "UNKNOWN").replace(":", "_").replace("/", "_")
    payload["written_at"] = _utc_now()

    # Per-symbol rolling window
    symbol_dir = SIGNAL_DIR / "by_symbol" / symbol
    symbol_dir.mkdir(parents=True, exist_ok=True)
    events_path = symbol_dir / "latest.json"
    events: list[dict] = []
    if events_path.exists():
        try:
            events = json.loads(events_path.read_text())
        except (json.JSONDecodeError, OSError):
            events = []
    events.append(payload)
    events = events[-MAX_EVENTS:]
    events_path.write_text(json.dumps(events, indent=2))

    # Global rolling window
    SIGNAL_DIR.mkdir(parents=True, exist_ok=True)
    global_path = SIGNAL_DIR / "latest.json"
    global_events: list[dict] = []
    if global_path.exists():
        try:
            global_events = json.loads(global_path.read_text())
        except (json.JSONDecodeError, OSError):
            global_events = []
    global_events.append(payload)
    global_events = global_events[-MAX_EVENTS:]
    global_path.write_text(json.dumps(global_events, indent=2))

    # Update runtime registry (non-blocking)
    try:
        from modules.data_center.runtime_registry import update_producer_last_write
        update_producer_last_write(
            producer_id="signal_event.tradingview_cdp.v1",
            contract_class="signal_event.v1",
            output_path=str(global_path),
            status="ok",
            evidence={"last_event": payload.get("event"), "symbol": symbol},
        )
    except Exception:
        pass

    return {
        "ok": True,
        "symbol": symbol,
        "event": payload.get("event", "?"),
        "total_events": len(global_events),
        "symbol_events": len(events),
    }
