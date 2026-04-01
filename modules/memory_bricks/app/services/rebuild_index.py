from __future__ import annotations

import json
import re

from app.core.paths import get_index_dir
from app.renderers.index_renderer import render_index_short
from app.storage.markdown_store import load_all_bricks


def rebuild_index() -> list[str]:
    bricks = load_all_bricks()
    index_dir = get_index_dir()
    short_path = index_dir / "index_short.md"
    full_path = index_dir / "index_full.json"

    short_path.write_text(render_index_short(bricks), encoding="utf-8")
    full_path.write_text(
        json.dumps([b.to_dict() for b in bricks], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    outputs = [str(short_path), str(full_path)]

    for group_name, key in [
        ("by_project", "project"),
        ("by_module", "module"),
        ("by_machine", "machine"),
        ("by_ia", "ia"),
    ]:
        base = index_dir / group_name
        for existing in base.glob("*.json"):
            existing.unlink()
        grouped = {}
        for brick in bricks:
            grouped.setdefault(getattr(brick, key) or "unknown", []).append(brick.to_dict())
        for bucket, items in grouped.items():
            out = base / f"{_bucket_name(bucket)}.json"
            out.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
            outputs.append(str(out))
    return outputs


def _bucket_name(value: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip())
    sanitized = re.sub(r"-{2,}", "-", sanitized).strip("-")
    return sanitized or "unknown"
