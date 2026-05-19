from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .models import RawEvent, EnrichedEvent


def ensure_parent_dir(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def read_jsonl(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.is_file():
        return []
    entries = []
    with open(p, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    return entries


def existing_ids(path: str | Path) -> set[str]:
    ids = set()
    for entry in read_jsonl(path):
        eid = entry.get("event_id")
        if eid:
            ids.add(eid)
    return ids


def append_raw_event(event: RawEvent, path: str | Path) -> str:
    path = Path(path)
    ensure_parent_dir(path)

    if event.event_id in existing_ids(path):
        return "skipped_duplicate"

    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

    return "appended"


def tail_jsonl(path: str | Path, n: int = 10) -> list[dict]:
    entries = read_jsonl(path)
    return entries[-n:] if entries else []


def append_enriched_event(event: EnrichedEvent, path: str | Path) -> str:
    path = Path(path)
    ensure_parent_dir(path)

    if event.event_id in existing_ids(path):
        return "skipped_duplicate"

    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(event.to_dict(), ensure_ascii=False) + "\n")

    return "appended"
