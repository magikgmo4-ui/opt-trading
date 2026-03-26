from __future__ import annotations

from app.core.constants import ALLOWED_STATUSES
from app.renderers.brick_renderer import render_brick
from app.storage.markdown_store import load_brick, overwrite_brick


def update_status(brick_id: str, new_status: str) -> tuple[str, str]:
    if new_status not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status: {new_status}")
    brick = load_brick(brick_id)
    before = brick.status
    brick.status = new_status
    brick.validate()
    content = render_brick(brick)
    overwrite_brick(brick, content)
    return before, brick.status
