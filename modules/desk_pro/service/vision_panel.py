from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

VISION_CONTEXT_LATEST = Path(
    "data/deskpro/inputs/vision_context/coinglass/latest.json"
)


def _age_hours(screenshot_ts: str) -> Optional[float]:
    try:
        ts = datetime.fromisoformat(screenshot_ts.replace("Z", "+00:00"))
        return (datetime.now(tz=timezone.utc) - ts).total_seconds() / 3600
    except Exception:
        return None


def read_vision_panel_data(path: Optional[Path] = None) -> dict:
    """Read vision_context.coinglass.v1 and return panel-ready dict.

    Returns {"ok": False, "vision": None, "reason": "..."} on any failure.
    Returns {"ok": True, "vision": {...}, "age_hours": float|None} on success.
    Never raises.
    """
    p = path or VISION_CONTEXT_LATEST
    if not p.exists():
        return {"ok": False, "vision": None, "reason": "no_data"}

    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {"ok": False, "vision": None, "reason": "read_error"}

    if data.get("input_class") != "vision_context.coinglass.v1":
        return {"ok": False, "vision": None, "reason": "wrong_input_class"}

    age = _age_hours(data.get("screenshot_ts", ""))
    return {"ok": True, "vision": data, "age_hours": age}
