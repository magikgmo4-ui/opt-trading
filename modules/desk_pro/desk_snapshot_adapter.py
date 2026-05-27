from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


_INPUT_CLASS = "desk_snapshot.v1"


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


def normalize_desk_snapshot_v1(payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {"input_class": _INPUT_CLASS, "errors": ["payload is not a dict"]}

    v1: Dict[str, Any] = dict(payload)
    v1.setdefault("input_class", _INPUT_CLASS)
    v1.setdefault("errors", [])
    return v1


def validate_desk_snapshot_v1(snapshot: dict) -> Tuple[bool, List[str]]:
    if not isinstance(snapshot, dict):
        return False, ["snapshot is not a dict"]

    errors: List[str] = []
    blocking = False

    if _safe_str(snapshot.get("input_class")) not in ("", _INPUT_CLASS):
        errors.append(f"unexpected input_class: {snapshot.get('input_class')!r}")

    for field in ("symbol", "tf", "snapshot_ts", "path"):
        if not _safe_str(snapshot.get(field)):
            errors.append(f"desk_snapshot missing {field}")
            blocking = True

    ts = _safe_str(snapshot.get("snapshot_ts"))
    if ts and not _parse_iso(ts):
        errors.append(f"unparseable snapshot_ts: {ts!r}")
        blocking = True

    return not blocking, errors


def read_desk_snapshot_v1(path: Path | str) -> Optional[dict]:
    p = Path(path)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

    if not isinstance(data, dict):
        return None
    return normalize_desk_snapshot_v1(data)

