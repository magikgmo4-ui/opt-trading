from __future__ import annotations

from app.storage.markdown_store import load_all_bricks, load_brick_text


def find_bricks(text: str) -> list[str]:
    needle = text.strip().casefold()
    if not needle:
        raise ValueError("Query text cannot be empty")

    rows = []
    for brick in load_all_bricks():
        haystacks = [
            brick.id,
            brick.title,
            brick.summary_short,
            brick.resume_point,
            " ".join(brick.tags),
            load_brick_text(brick.id),
        ]
        if any(needle in value.casefold() for value in haystacks if value):
            rows.append(
                f"{brick.id} — {brick.date[:10]} — {brick.ia} — {brick.machine} — {brick.status} — {brick.module}"
            )
    return rows
