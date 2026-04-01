from __future__ import annotations

import json

from app.core.paths import get_exports_dir
from app.renderers.brick_renderer import render_brick
from app.storage.markdown_store import load_bricks_by_ids


def export_bricks(ids: list[str], fmt: str) -> str:
    bricks = load_bricks_by_ids(ids)
    normalized_ids = [brick.id for brick in bricks]
    if not normalized_ids:
        raise ValueError("No brick ids provided")
    out = get_exports_dir() / f"export_{'_'.join(normalized_ids)}.{fmt}"

    if fmt == "json":
        out.write_text(json.dumps([b.to_dict() for b in bricks], indent=2, ensure_ascii=False), encoding="utf-8")
    elif fmt == "md":
        out.write_text("\n\n".join(render_brick(brick).rstrip() for brick in bricks) + "\n", encoding="utf-8")
    else:
        lines = []
        for brick in bricks:
            lines.append(f"{brick.id} | {brick.date} | {brick.status} | {brick.title}")
            lines.append(f"  summary: {brick.summary_short}")
            lines.append(f"  resume: {brick.resume_point}")
            if brick.links:
                lines.append(f"  links: {', '.join(brick.links)}")
        out.write_text("\n".join(lines), encoding="utf-8")
    return str(out)
