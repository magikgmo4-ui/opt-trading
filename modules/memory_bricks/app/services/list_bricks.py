from __future__ import annotations

from app.storage.markdown_store import load_all_bricks


def list_bricks(filters: dict[str, str]) -> list[str]:
    rows = []
    for brick in load_all_bricks():
        if filters.get("status") and brick.status != filters["status"]:
            continue
        if filters.get("type") and brick.type != filters["type"]:
            continue
        if filters.get("project") and brick.project != filters["project"]:
            continue
        if filters.get("module") and brick.module != filters["module"]:
            continue
        if filters.get("machine") and brick.machine != filters["machine"]:
            continue
        if filters.get("ia") and brick.ia != filters["ia"]:
            continue
        if filters.get("surface") and brick.surface != filters["surface"]:
            continue
        if filters.get("tag") and filters["tag"] not in brick.tags:
            continue
        rows.append(
            f"{brick.id} — {brick.date[:10]} — {brick.ia} — {brick.machine} — {brick.status} — {brick.module}"
        )
    return rows
