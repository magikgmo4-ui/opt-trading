from __future__ import annotations

from pathlib import Path
from typing import Any

from modules.ipo_tracking.storage.jsonl_store import atomic_write_json


def write_spacex_view(path: Path, snapshot: dict[str, Any]) -> None:
    payload = {
        "input_class": "spacex_super_desk.v1",
        "provider_id": "ipo_tracking",
        "produced_at": snapshot.get("produced_at"),
        "symbol": snapshot.get("asset", {}).get("symbol", "SPCX"),
        "snapshot": snapshot,
    }
    atomic_write_json(path, payload)

    try:
        from modules.data_center.runtime_registry import update_producer_last_write
        update_producer_last_write(
            "ipo_tracking_spacex",
            "spacex_super_desk.v1",
            str(path),
            status="ok",
            evidence={"symbol": "SPCX", "mode": "monitor_only"},
        )
    except Exception:
        # Runtime registry is best-effort; the view remains the canonical local handoff.
        pass
