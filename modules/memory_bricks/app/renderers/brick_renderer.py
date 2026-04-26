from __future__ import annotations

from app.core.frontmatter import dump_frontmatter
from app.schemas.brick_schema import BrickModel


def render_brick(brick: BrickModel) -> str:
    data = brick.to_dict()
    front = dump_frontmatter(data).strip()

    decisions_md = "\n".join(f"- {item}" for item in brick.decisions) or "- "
    todo_md = "\n".join(f"- {item}" for item in brick.todo) or "- "
    links_md = "\n".join(f"- {item}" for item in brick.links) or "- "

    return (
        f"---\n{front}\n---\n\n"
        f"# {brick.id} — {brick.title}\n\n"
        f"## Résumé court\n{brick.summary_short}\n\n"
        f"## Décisions\n{decisions_md}\n\n"
        f"## TODO\n{todo_md}\n\n"
        f"## Reprise\n{brick.resume_point}\n\n"
        f"## Liens\n{links_md}\n"
    )
