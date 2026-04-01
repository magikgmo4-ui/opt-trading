from __future__ import annotations

from app.storage.markdown_store import load_brick_text


def show_brick(brick_id: str) -> str:
    return load_brick_text(brick_id)
