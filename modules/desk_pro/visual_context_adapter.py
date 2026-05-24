from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


_INPUT_CLASS = "visual_context.v1"


def _safe_str(v: Any) -> str:
    if v is None:
        return ""
    return str(v).strip()


def _parse_iso(ts: str) -> bool:
    if not ts:
        return False
    try:
        if ts.endswith("Z"):
            datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            datetime.fromisoformat(ts)
        return True
    except Exception:
        return False


def normalize_visual_context_v1(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {"input_class": _INPUT_CLASS, "errors": ["payload is not a dict"]}

    v1: Dict[str, Any] = dict(payload)
    v1.setdefault("input_class", _INPUT_CLASS)
    v1.setdefault("errors", [])
    return v1


def validate_visual_context_v1(visual_context: dict) -> Tuple[bool, List[str]]:
    if not isinstance(visual_context, dict):
        return False, ["visual_context is not a dict"]

    errors: List[str] = []
    blocking = False

    if _safe_str(visual_context.get("input_class")) not in ("", _INPUT_CLASS):
        errors.append(f"unexpected input_class: {visual_context.get('input_class')!r}")

    for field in ("source", "capture_id", "symbol", "timeframe", "captured_at", "image_ref", "status"):
        if not _safe_str(visual_context.get(field)):
            errors.append(f"visual_context missing {field}")
            blocking = True

    captured_at = _safe_str(visual_context.get("captured_at"))
    if captured_at and not _parse_iso(captured_at):
        errors.append(f"unparseable captured_at: {captured_at!r}")
        blocking = True

    return not blocking, errors


def read_visual_context_v1(path: Path | str) -> Optional[dict]:
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(data, dict):
        return None
    return normalize_visual_context_v1(data)

