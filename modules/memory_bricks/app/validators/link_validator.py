from __future__ import annotations

from app.storage.markdown_store import load_brick


def validate_link_target(brick_id: str) -> None:
    load_brick(brick_id)
