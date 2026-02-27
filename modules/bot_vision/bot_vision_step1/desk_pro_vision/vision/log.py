from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

@dataclass
class LogEvent:
    ts: str
    lvl: str
    step: str
    ok: bool
    data: Dict[str, Any]

def now_iso_local(tz_offset: str = "-05:00") -> str:
    # We keep local offset as string for now. In later steps we’ll use zoneinfo.
    dt = datetime.now().astimezone()
    return dt.isoformat()

class JsonlLogger:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, lvl: str, step: str, ok: bool, **data: Any) -> None:
        ev = LogEvent(ts=now_iso_local(), lvl=lvl, step=step, ok=ok, data=data)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(ev), ensure_ascii=False) + "\n")
