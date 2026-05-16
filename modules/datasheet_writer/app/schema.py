from __future__ import annotations
from dataclasses import dataclass


@dataclass
class WriteResult:
    ok: bool
    dry_run: bool
    written: bool
    jsonl_path: str = ""
    csv_path: str = ""
    error: str = ""
