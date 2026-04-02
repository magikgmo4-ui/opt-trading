from __future__ import annotations

from app.renderers.brick_renderer import render_brick
from app.storage.markdown_store import load_brick, overwrite_brick


def link_bricks(source_id: str, target_id: str) -> None:
    if source_id == target_id:
        raise ValueError("Cannot create self-link")
    source = load_brick(source_id)
    _ = load_brick(target_id)  # validate target exists
    if target_id not in source.links:
        source.links.append(target_id)
        source.links.sort()
    source.validate()
    content = render_brick(source)
    overwrite_brick(source, content)
