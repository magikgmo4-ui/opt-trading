from __future__ import annotations

from app.schemas.brick_schema import BrickModel


def render_merge(bricks: list[BrickModel]) -> str:
    decisions = []
    todos = []
    final_resume = ""
    for brick in bricks:
        decisions.extend(item for item in brick.decisions if item not in decisions)
        todos.extend(item for item in brick.todo if item not in todos)
        if brick.resume_point:
            final_resume = brick.resume_point

    lines = ["MERGE MEMORY BRICKS", "", "Sources:"]
    for brick in bricks:
        lines.append(f"- {brick.id}")
    lines.extend(["", "Chronologie:"])
    for idx, brick in enumerate(bricks, start=1):
        lines.append(f"{idx}. {brick.id} — {brick.title} — {brick.summary_short}")

    lines.extend(["", "Décisions agrégées:"])
    for item in decisions or ["-"]:
        lines.append(f"- {item}" if item != "-" else item)

    lines.extend(["", "TODO agrégés:"])
    for item in todos or ["-"]:
        lines.append(f"- {item}" if item != "-" else item)

    lines.extend(["", "Point de reprise:", final_resume or "-"])
    return "\n".join(lines) + "\n"
