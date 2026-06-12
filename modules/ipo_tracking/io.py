from __future__ import annotations
import json, tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default

def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)

def append_jsonl(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")
