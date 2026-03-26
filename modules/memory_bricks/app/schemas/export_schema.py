from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ExportResult:
    output_path: str
    format: str
    brick_ids: list[str]
