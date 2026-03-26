from __future__ import annotations

from app.schemas.brick_schema import BrickModel


def render_index_short(bricks: list[BrickModel]) -> str:
    lines = ["# INDEX BRIQUES", ""]
    for brick in sorted(bricks, key=lambda b: b.date):
        lines.append(f"{brick.id} — {brick.date[:10]} — {brick.ia} — {brick.machine} — {brick.status} — {brick.module}")
    lines.append("")
    return "\n".join(lines)
