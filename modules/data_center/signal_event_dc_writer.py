"""
signal_event_dc_writer.py — route webhook events (state/events.jsonl) to data_center.

Produces:
    signal_event.v1 — per-symbol views with latest signal events
    Writes to: data/data_center/views/signal_event/by_symbol/{SYM}.json
               data/data_center/views/signal_event/latest.json

Usage:
    python -m modules.data_center.signal_event_dc_writer
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_EVENTS_PATH = _PROJECT_ROOT / "state" / "events.jsonl"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def produce_signal_event_views() -> dict:
    """Read events.jsonl and publish per-symbol views to data_center."""
    if not _EVENTS_PATH.exists():
        return {"error": "events.jsonl not found"}

    now = datetime.now(timezone.utc).isoformat()
    by_symbol: dict[str, list[dict]] = {}

    for line in _EVENTS_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            evt = json.loads(line)
        except json.JSONDecodeError:
            continue

        sym = evt.get("symbol", "")
        if not sym:
            continue

        by_symbol.setdefault(sym, []).append({
            "engine": evt.get("engine", ""),
            "signal": evt.get("signal", ""),
            "price": evt.get("price"),
            "tp": evt.get("tp"),
            "sl": evt.get("sl"),
            "qty": evt.get("qty"),
            "reason": evt.get("reason", ""),
            "ts": evt.get("_ts", ""),
        })

    # Write per-symbol views
    for sym, events in by_symbol.items():
        sym_dir = _VIEWS_DIR / "signal_event" / "by_symbol" / sym.replace("/", "_")
        sym_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "input_class": "signal_event.v1",
            "provider_id": "webhook_server",
            "symbol": sym,
            "produced_at": now,
            "total_events": len(events),
            "latest": events[-1] if events else None,
            "events": events[-50:],  # Last 50
        }
        _atomic_write(sym_dir / "latest.json", payload)

    # Global latest
    global_payload = {
        "input_class": "signal_event.v1",
        "provider_id": "webhook_server",
        "produced_at": now,
        "total_events": sum(len(v) for v in by_symbol.values()),
        "total_symbols": len(by_symbol),
        "symbols": sorted(by_symbol.keys()),
    }
    _atomic_write(_VIEWS_DIR / "signal_event" / "latest.json", global_payload)

    # Runtime registry
    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write(
        producer_id="webhook_server",
        contract_class="signal_event.v1",
        output_path=str(_VIEWS_DIR / "signal_event" / "latest.json"),
        status="ok",
        evidence={"symbols": len(by_symbol), "events": global_payload["total_events"]},
    )

    return global_payload


if __name__ == "__main__":
    result = produce_signal_event_views()
    if "error" in result:
        print("ERROR:", result["error"])
    else:
        print(f"signal_event.v1: {result['total_symbols']} symbols, {result['total_events']} events")
