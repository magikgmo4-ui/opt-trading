from __future__ import annotations

import json

from app.core.paths import ensure_state_dirs, get_sequence_path


def next_brick_id() -> str:
    ensure_state_dirs()
    seq_path = get_sequence_path()
    data = _read_sequence(seq_path)
    last = int(data.get("last", 0)) + 1
    data["last"] = last
    seq_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return f"MB-{last:05d}"


def _read_sequence(seq_path) -> dict[str, int]:
    if not seq_path.exists():
        return {"last": 0}
    try:
        data = json.loads(seq_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid sequence file: {seq_path}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Invalid sequence payload: {seq_path}")
    if "last" not in data:
        data["last"] = 0
    return data
