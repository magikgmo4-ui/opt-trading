from __future__ import annotations

from app.core.paths import get_handoffs_dir
from app.renderers.handoff_renderer import render_handoff
from app.storage.markdown_store import load_bricks_by_ids


def handoff_bricks(ids: list[str], target: str) -> str:
    bricks = load_bricks_by_ids(ids)
    if not bricks:
        raise ValueError("No brick ids provided")
    content = render_handoff(bricks, target)
    out = get_handoffs_dir() / f"handoff_{target}_{'_'.join(brick.id for brick in bricks)}.txt"
    out.write_text(content, encoding="utf-8")
    return str(out)
