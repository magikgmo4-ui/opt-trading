"""
position_state_dc_writer.py — route position state to data_center.

Reads state/positions.json and publishes to data_center/views/position_state/.

Usage:
    python -m modules.data_center.position_state_dc_writer
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_POSITIONS_PATH = _PROJECT_ROOT / "state" / "positions.json"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def produce_position_state() -> dict:
    now = datetime.now(timezone.utc).isoformat()
    positions = {}
    if _POSITIONS_PATH.exists():
        try:
            positions = json.loads(_POSITIONS_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass

    _atomic_write(_VIEWS_DIR / "position_state" / "latest.json", {
        "input_class": "position_state.v1",
        "provider_id": "position_engine",
        "produced_at": now,
        "positions": positions,
    })

    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write("position_engine", "position_state.v1",
        str(_VIEWS_DIR / "position_state" / "latest.json"), "ok")
    return {"produced_at": now, "positions": len(positions) if isinstance(positions, dict) else 0}


if __name__ == "__main__":
    r = produce_position_state()
    print(f"Position state: {r['positions']} positions")
