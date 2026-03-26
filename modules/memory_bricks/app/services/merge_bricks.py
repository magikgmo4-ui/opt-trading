from __future__ import annotations

from pathlib import Path

from app.core.paths import get_exports_dir
from app.renderers.merge_renderer import render_merge
from app.storage.markdown_store import load_bricks_by_ids


def merge_bricks(ids: list[str]) -> str:
    bricks = load_bricks_by_ids(ids)
    bricks.sort(key=lambda b: b.date)
    content = render_merge(bricks)
    output = get_exports_dir() / f"merge_{'_'.join(ids)}.txt"
    output.write_text(content, encoding="utf-8")
    return str(output)
