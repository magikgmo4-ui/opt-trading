from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

VISION_ANALYSIS_LATEST = Path(
    "data/deskpro/inputs/vision_analysis/latest.json"
)


def read_vision_analysis(path: Optional[Path] = None) -> Optional[dict]:
    """Read vision_analysis.v1 from a local JSON file.

    Default path: data/deskpro/inputs/vision_analysis/latest.json
    When path= is explicit, that path is used directly.

    Returns the payload dict if valid, None otherwise.
    Never raises. Never calls API, OCR, browser, or any vision model.
    Absent or malformed file → None (caller treats as missing).
    """
    p = path or VISION_ANALYSIS_LATEST
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    if data.get("input_class") != "vision_analysis.v1":
        return None
    return data
